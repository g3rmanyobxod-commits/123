package com.globe.vpn;

import android.app.Notification;
import android.app.PendingIntent;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.VpnService;
import android.os.Build;
import android.os.ParcelFileDescriptor;
import go.Seq;
import libv2ray.CoreCallbackHandler;
import libv2ray.CoreController;
import libv2ray.Libv2ray;

/* loaded from: classes.dex */
public class GlobeVpnService extends VpnService {
    public static final String ACTION_START = "com.globe.vpn.START";
    public static final String ACTION_STOP = "com.globe.vpn.STOP";
    private static final String CHANNEL = "vpn";
    public static final String EXTRA_CONFIG = "config";
    public static final String EXTRA_NAME = "name";
    private static final int NOTIFY_ID = 4101;
    public static final String STATE_CONNECTED = "connected";
    public static final String STATE_CONNECTING = "connecting";
    public static final String STATE_ERROR = "error";
    public static final String STATE_IDLE = "idle";
    private static final String TRAFFIC_TAG = "proxy";
    static volatile String activeName = "";
    static volatile GlobeVpnService instance;
    static volatile String noticeServer = "";
    static volatile int noticePing = -1;
    static volatile long connectedAt = 0;
    static volatile long downBytes = 0;
    static volatile String lastError = "";
    static volatile String state = "idle";
    static volatile long upBytes;
    private CoreController core;
    private volatile boolean running = false;
    private Thread statsThread;
    private ParcelFileDescriptor tunnel;

    static void reset() {
        state = STATE_IDLE;
        lastError = "";
        activeName = "";
        upBytes = 0L;
        downBytes = 0L;
        connectedAt = 0L;
    }

    @Override // android.app.Service
    public void onCreate() {
        super.onCreate();
        instance = this;
        createChannel();
        try {
            Seq.setContext(getApplicationContext());
        } catch (Throwable unused) {
        }
    }

    @Override // android.app.Service
    public int onStartCommand(Intent intent, int i, int i2) {
        if (intent != null && ACTION_STOP.equals(intent.getAction())) {
            stopEverything();
            stopSelf();
            return 2;
        }
        String stringExtra = intent == null ? null : intent.getStringExtra(EXTRA_CONFIG);
        String stringExtra2 = intent == null ? "" : intent.getStringExtra(EXTRA_NAME);
        if (stringExtra == null || stringExtra.isEmpty()) {
            SharedPreferences sharedPreferences = getSharedPreferences("globe-vpn", 0);
            stringExtra = sharedPreferences.getString("last_config", null);
            stringExtra2 = sharedPreferences.getString("last_name", "");
        }
        if (stringExtra == null || stringExtra.isEmpty()) {
            state = STATE_ERROR;
            lastError = "Нет конфигурации";
            stopSelf();
            return 2;
        }
        getSharedPreferences("globe-vpn", 0).edit().putString("last_config", stringExtra).putString("last_name", stringExtra2 == null ? "" : stringExtra2).apply();
        startForegroundSafely(stringExtra2);
        if (prepare(this) != null) {
            state = STATE_ERROR;
            lastError = "Разрешение VPN не выдано";
            stopSelf();
            return 2;
        }
        state = STATE_CONNECTING;
        lastError = "";
        if (stringExtra2 == null) {
            stringExtra2 = "";
        }
        activeName = stringExtra2;
        try {
            stopCore();
            ParcelFileDescriptor parcelFileDescriptor = this.tunnel;
            if (parcelFileDescriptor != null) {
                try {
                    parcelFileDescriptor.close();
                } catch (Exception unused) {
                }
                this.tunnel = null;
            }
            VpnService.Builder builder = new Builder();
            builder.setSession("smpl");
            builder.setMtu(1500);
            builder.addAddress("10.10.14.1", 30);
            builder.addRoute("0.0.0.0", 0);
            builder.addAddress("fc00::10:10:14:1", 126);
            builder.addRoute("::", 0);
            builder.addDnsServer("1.1.1.1");
            builder.addDnsServer("8.8.8.8");
            builder.addDnsServer("1.0.0.1");
            if (Build.VERSION.SDK_INT >= 29) {
                builder.setMetered(false);
            }
            try {
                builder.addDisallowedApplication(getPackageName());
            } catch (Exception unused2) {
            }
            ParcelFileDescriptor establish = builder.establish();
            this.tunnel = establish;
            if (establish != null) {
                Libv2ray.initCoreEnv(getFilesDir().getAbsolutePath(), "");
                this.core = Libv2ray.newCoreController(new CoreCallbackHandler() { // from class: com.globe.vpn.GlobeVpnService.1
                    @Override // libv2ray.CoreCallbackHandler
                    public long startup() {
                        GlobeVpnService.state = GlobeVpnService.STATE_CONNECTED;
                        GlobeVpnService.connectedAt = System.currentTimeMillis();
                        return 0L;
                    }

                    @Override // libv2ray.CoreCallbackHandler
                    public long shutdown() {
                        if (!GlobeVpnService.STATE_CONNECTED.equals(GlobeVpnService.state)) {
                            return 0L;
                        }
                        GlobeVpnService.state = GlobeVpnService.STATE_IDLE;
                        return 0L;
                    }

                    @Override // libv2ray.CoreCallbackHandler
                    public long onEmitStatus(long j, String str) {
                        if (str == null || !str.toLowerCase().contains("fail")) {
                            return 0L;
                        }
                        GlobeVpnService.lastError = str;
                        return 0L;
                    }
                });
                final int fd = this.tunnel.getFd();
                final String configForThread = stringExtra;
                final CoreController coreController = this.core;
                this.running = true;
                new Thread(new Runnable() { // from class: com.globe.vpn.GlobeVpnService.2
                    @Override // java.lang.Runnable
                    public void run() {
                        try {
                            coreController.startLoop(configForThread, fd);
                        } catch (Throwable th) {
                            String message = th.getMessage();
                            if (message == null) {
                                message = th.getClass().getSimpleName();
                            }
                            GlobeVpnService.lastError = message;
                            GlobeVpnService.this.stopEverything();
                            GlobeVpnService.state = GlobeVpnService.STATE_ERROR;
                            GlobeVpnService.this.stopSelf();
                        }
                    }
                }, "globe-vpn-core").start();
                startStats();
                notifyState(activeName);
                return 1;
            }
            state = STATE_ERROR;
            lastError = "Не удалось создать tun-интерфейс";
            stopSelf();
            return 2;
        } catch (Throwable th) {
            state = STATE_ERROR;
            String message = th.getMessage();
            if (message == null) {
                message = th.getClass().getSimpleName();
            }
            lastError = message;
            stopCore();
            ParcelFileDescriptor parcelFileDescriptor2 = this.tunnel;
            if (parcelFileDescriptor2 != null) {
                try {
                    parcelFileDescriptor2.close();
                } catch (Exception unused3) {
                }
                this.tunnel = null;
            }
            stopSelf();
            return 2;
        }
    }

    @Override // android.net.VpnService
    public void onRevoke() {
        stopEverything();
        stopSelf();
        super.onRevoke();
    }

    private void startStats() {
        if (this.statsThread != null) {
            return;
        }
        Thread thread = new Thread(new Runnable() { // from class: com.globe.vpn.GlobeVpnService.3
            @Override // java.lang.Runnable
            public void run() {
                while (GlobeVpnService.this.running && GlobeVpnService.this.core != null) {
                    try {
                        String queryAllOutboundTrafficStats = GlobeVpnService.this.core.queryAllOutboundTrafficStats();
                        if (queryAllOutboundTrafficStats != null && !queryAllOutboundTrafficStats.isEmpty()) {
                            long j = 0;
                            long j2 = 0;
                            for (String str : queryAllOutboundTrafficStats.split(";")) {
                                String[] split = str.split(",");
                                if (split.length == 3 && GlobeVpnService.TRAFFIC_TAG.equals(split[0])) {
                                    try {
                                        long parseLong = Long.parseLong(split[2]);
                                        if ("uplink".equals(split[1])) {
                                            j += parseLong;
                                        } else if ("downlink".equals(split[1])) {
                                            j2 += parseLong;
                                        }
                                    } catch (NumberFormatException unused) {
                                    }
                                }
                            }
                            GlobeVpnService.upBytes = j;
                            GlobeVpnService.downBytes = j2;
                        }
                    } catch (Throwable unused2) {
                    }
                    try {
                        Thread.sleep(1000L);
                    } catch (InterruptedException unused3) {
                        return;
                    }
                }
            }
        }, "globe-vpn-stats");
        this.statsThread = thread;
        thread.setDaemon(true);
        this.statsThread.start();
    }

    private void stopCore() {
        this.running = false;
        try {
            CoreController coreController = this.core;
            if (coreController != null) {
                coreController.stopLoop();
            }
        } catch (Throwable unused) {
        }
        this.core = null;
        Thread thread = this.statsThread;
        if (thread != null) {
            thread.interrupt();
            this.statsThread = null;
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void stopEverything() {
        stopCore();
        ParcelFileDescriptor parcelFileDescriptor = this.tunnel;
        if (parcelFileDescriptor != null) {
            try {
                parcelFileDescriptor.close();
            } catch (Exception unused) {
            }
            this.tunnel = null;
        }
        state = STATE_IDLE;
        activeName = "";
        upBytes = 0L;
        downBytes = 0L;
        connectedAt = 0L;
        try {
            stopForeground(true);
        } catch (Throwable unused2) {
        }
        NotificationManager notificationManager = (NotificationManager) getSystemService("notification");
        if (notificationManager != null) {
            notificationManager.cancel(NOTIFY_ID);
        }
    }

    @Override // android.app.Service
    public void onDestroy() {
        stopEverything();
        instance = null;
        super.onDestroy();
    }

    private void createChannel() {
        NotificationManager notificationManager;
        if (Build.VERSION.SDK_INT >= 26 && (notificationManager = (NotificationManager) getSystemService("notification")) != null) {
            NotificationChannel notificationChannel = new NotificationChannel(CHANNEL, "VPN", 2);
            notificationChannel.setShowBadge(false);
            notificationManager.createNotificationChannel(notificationChannel);
        }
    }


    private android.app.PendingIntent stopIntent() {
        Intent intent = new Intent(this, GlobeVpnService.class);
        intent.setAction(ACTION_STOP);
        return android.app.PendingIntent.getService(this, 7, intent,
                android.app.PendingIntent.FLAG_UPDATE_CURRENT | android.app.PendingIntent.FLAG_IMMUTABLE);
    }

    private void attachStopAction(Notification.Builder builder) {
        try {
            builder.addAction(new Notification.Action.Builder(
                    android.graphics.drawable.Icon.createWithResource(this, R.drawable.ic_stat_vpn),
                    "Выключить", stopIntent()).build());
        } catch (Throwable ignored) {
        }
    }

    private void startForegroundSafely(String label) {
        try {
            Notification.Builder builder;
            if (Build.VERSION.SDK_INT >= 26) {
                builder = new Notification.Builder(this, CHANNEL);
            } else {
                builder = new Notification.Builder(this);
            }
            Intent intent = new Intent(this, MainActivity.class);
            intent.setFlags(0x14000000);
            PendingIntent pending = PendingIntent.getActivity(this, 0, intent, 0x0c000000);
            String text = (label == null || label.isEmpty()) ? "Туннель активен" : "Подключено: " + label;
            builder.setContentTitle("smpl")
                    .setContentText(text)
                    .setSmallIcon(R.drawable.ic_stat_vpn)
                    .setOngoing(true)
                    .setContentIntent(pending);
            attachStopAction(builder);
            Notification notification = builder.build();
            if (Build.VERSION.SDK_INT >= 29) {
                startForeground(4101, notification, 0x40000000);
            } else {
                startForeground(4101, notification);
            }
        } catch (Throwable ignored) {
        }
    }

    private void notifyState(String str) {
        try {
            NotificationManager notificationManager = (NotificationManager) getSystemService("notification");
            if (notificationManager == null) {
                return;
            }
            Notification.Builder builder = Build.VERSION.SDK_INT >= 26
                    ? new Notification.Builder(this, CHANNEL)
                    : new Notification.Builder(this);
            builder.setContentTitle("smpl");
            builder.setContentIntent(android.app.PendingIntent.getActivity(this, 0,
                    new Intent(this, MainActivity.class).setFlags(0x14000000),
                    android.app.PendingIntent.FLAG_UPDATE_CURRENT | android.app.PendingIntent.FLAG_IMMUTABLE));
            attachStopAction(builder);
            String name = noticeServer != null && !noticeServer.isEmpty()
                    ? noticeServer
                    : (str == null || str.isEmpty() ? "Туннель активен" : str);
            String line = noticePing >= 0 ? name + " · " + noticePing + " мс" : name;
            builder.setContentText(line).setSmallIcon(R.drawable.ic_stat_vpn).setOngoing(true);
            notificationManager.notify(NOTIFY_ID, builder.build());
        } catch (Throwable ignored) {
        }
    }

    /* v3: обновление уведомления, когда меняется пинг */
    void refreshNotice() {
        notifyState(activeName);
    }
}
