package com.globe.vpn;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.drawable.Drawable;
import android.util.Base64;
import android.graphics.Color;
import android.net.Uri;
import android.net.VpnService;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Iterator;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import org.json.JSONArray;
import org.json.JSONObject;

/* loaded from: classes.dex */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int REQ_OPEN = 42;
    private static final int REQ_SAVE = 41;
    private static final int REQ_VPN = 43;
    private static final String START_URL = "https://appassets.androidplatform.net/assets/vpn.html";
    private WebView web;
    private long lastBackAt = 0;
    private String pendingSaveText = "";
    public static final String EXTRA_RECONNECT = "globe_reconnect";
    private boolean pendingReconnect = false;
    private String pendingVpnConfig = null;
    private String pendingVpnName = "";
    private final Handler ui = new Handler(Looper.getMainLooper());
    private boolean polling = false;
    private final ExecutorService pool = Executors.newFixedThreadPool(6);
    private String pendingLink = null;

    // Android 13+: без разрешения уведомления (в том числе статус VPN) не показываются
    void requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= 33
                && checkSelfPermission("android.permission.POST_NOTIFICATIONS") != 0) {
            requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"}, 4103);
        }
    }

    @Override // android.app.Activity
    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        checkReconnect(getIntent());
        Window window = getWindow();
        window.setStatusBarColor(Color.parseColor("#F2F0EA"));
        window.setNavigationBarColor(Color.parseColor("#F2F0EA"));
        setLightSystemBars(true);
        requestNotificationPermission();
        WebView webView = new WebView(this);
        this.web = webView;
        webView.setBackgroundColor(Color.parseColor("#F2F0EA"));
        this.web.setOverScrollMode(2);
        this.web.setLongClickable(false);
        this.web.setHapticFeedbackEnabled(true);
        this.web.setOnLongClickListener(new View.OnLongClickListener() { // from class: com.globe.vpn.MainActivity.1
            @Override // android.view.View.OnLongClickListener
            public boolean onLongClick(View view) {
                return true;
            }
        });
        WebSettings settings = this.web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setCacheMode(-1);
        settings.setTextZoom(100);
        settings.setUseWideViewPort(false);
        settings.setLoadWithOverviewMode(false);
        if (Build.VERSION.SDK_INT >= 26) {
            settings.setSafeBrowsingEnabled(false);
        }
        this.web.addJavascriptInterface(new Bridge(), "Native");
        this.web.setWebChromeClient(new WebChromeClient() {
            @Override // android.webkit.WebChromeClient
            public void onPermissionRequest(final android.webkit.PermissionRequest request) {
                runOnUiThread(new Runnable() {
                    @Override // java.lang.Runnable
                    public void run() {
                        request.grant(request.getResources());
                    }
                });
            }
        });
        this.web.setWebViewClient(new WebViewClient() { // from class: com.globe.vpn.MainActivity.2
            @Override // android.webkit.WebViewClient
            public WebResourceResponse shouldInterceptRequest(WebView webView2, WebResourceRequest webResourceRequest) {
                String str;
                Uri url = webResourceRequest.getUrl();
                if (url == null || !MainActivity.HOST.equals(url.getHost())) {
                    return null;
                }
                String path = url.getPath() == null ? "" : url.getPath();
                if (!path.startsWith("/assets/")) {
                    return null;
                }
                String substring = path.substring(8);
                try {
                    InputStream open = MainActivity.this.getAssets().open(substring);
                    if (substring.endsWith(".html")) {
                        str = "text/html";
                    } else if (substring.endsWith(".js")) {
                        str = "application/javascript";
                    } else {
                        str = substring.endsWith(".css") ? "text/css" : "application/octet-stream";
                    }
                    return new WebResourceResponse(str, "UTF-8", open);
                } catch (Exception unused) {
                    return new WebResourceResponse("text/plain", "UTF-8", new ByteArrayInputStream("".getBytes()));
                }
            }

            @Override // android.webkit.WebViewClient
            public boolean shouldOverrideUrlLoading(WebView webView2, WebResourceRequest webResourceRequest) {
                Uri url = webResourceRequest.getUrl();
                String lowerCase = url == null ? "" : String.valueOf(url.getScheme()).toLowerCase();
                if (!lowerCase.equals("http") && !lowerCase.equals("https")) {
                    return false;
                }
                MainActivity.this.openExternally(url);
                return true;
            }

            @Override // android.webkit.WebViewClient
            public void onPageFinished(WebView webView2, String str) {
                if (str == null || !str.startsWith("https://appassets.androidplatform.net")) {
                    return;
                }
                webView2.evaluateJavascript("window.__APP = { version: '1.0.0', platform: 'android' };", null);
                MainActivity.this.deliverReconnect();
                MainActivity.this.deliverPendingLink();
            }
        });
        setContentView(this.web);
        if (bundle == null) {
            this.web.loadUrl(START_URL);
        } else {
            this.web.restoreState(bundle);
        }
    }

    /* v3: заголовки подписки → строки «# ключ: значение», их разбирает интерфейс */
    private static String metaHeaders(HttpURLConnection connection) {
        StringBuilder sb = new StringBuilder();
        String[] names = {"profile-title", "profile-desc", "profile-description", "announce",
                "profile-update-interval", "subscription-userinfo"};
        for (String name : names) {
            String value = connection.getHeaderField(name);
            if (value != null && !value.trim().isEmpty()) {
                sb.append("# ").append(name).append(": ").append(value.trim()).append('\n');
            }
        }
        return sb.toString();
    }

    @Override // android.app.Activity
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        checkReconnect(intent);
        deliverReconnect();
        deliverPendingLink();
    }

    // флаг «Включить» из уведомления: запоминаем и передаём интерфейсу, когда страница готова
    private void checkReconnect(Intent intent) {
        if (intent != null && intent.getBooleanExtra(EXTRA_RECONNECT, false)) {
            intent.removeExtra(EXTRA_RECONNECT);
            pendingReconnect = true;
        }
    }

    private void deliverReconnect() {
        if (pendingReconnect && this.web != null) {
            pendingReconnect = false;
            this.web.evaluateJavascript("window.__onNotifyReconnect && window.__onNotifyReconnect()", null);
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void deliverPendingLink() {
        Intent intent = getIntent();
        Uri data = intent == null ? null : intent.getData();
        if (data == null) {
            if (this.pendingLink == null) {
                return;
            }
        } else {
            this.pendingLink = data.toString();
            intent.setData(null);
        }
        final String str = this.pendingLink;
        if (str == null || this.web == null) {
            return;
        }
        runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.3
            @Override // java.lang.Runnable
            public void run() {
                MainActivity.this.web.evaluateJavascript("window.__importLink && window.__importLink(" + JSONObject.quote(str) + ")", null);
                MainActivity.this.pendingLink = null;
            }
        });
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void openExternally(Uri uri) {
        try {
            startActivity(new Intent("android.intent.action.VIEW", uri));
        } catch (Exception unused) {
            toast("Не удалось открыть ссылку");
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void setLightSystemBars(boolean z) {
        int i;
        View decorView = getWindow().getDecorView();
        int systemUiVisibility = decorView.getSystemUiVisibility();
        if (z) {
            i = systemUiVisibility | 8192;
            if (Build.VERSION.SDK_INT >= 26) {
                i = systemUiVisibility | 8208;
            }
        } else {
            i = systemUiVisibility & (-8193);
            if (Build.VERSION.SDK_INT >= 26) {
                i = systemUiVisibility & (-8209);
            }
        }
        decorView.setSystemUiVisibility(i);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void startVpn(String str, String str2) {
        Intent intent = new Intent(this, (Class<?>) GlobeVpnService.class);
        intent.setAction(GlobeVpnService.ACTION_START);
        intent.putExtra(GlobeVpnService.EXTRA_CONFIG, str);
        if (str2 == null) {
            str2 = "";
        }
        intent.putExtra(GlobeVpnService.EXTRA_NAME, str2);
        if (Build.VERSION.SDK_INT >= 26) {
            startForegroundService(intent);
        } else {
            startService(intent);
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void stopVpn() {
        Intent intent = new Intent(this, (Class<?>) GlobeVpnService.class);
        intent.setAction(GlobeVpnService.ACTION_STOP);
        try {
            startService(intent);
        } catch (Exception unused) {
            stopService(intent);
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    public String vpnStateJson() {
        JSONObject jSONObject = new JSONObject();
        try {
            jSONObject.put("state", GlobeVpnService.state);
            jSONObject.put(GlobeVpnService.STATE_ERROR, GlobeVpnService.lastError);
            jSONObject.put(GlobeVpnService.EXTRA_NAME, new String(GlobeVpnService.activeName.getBytes("UTF-8"), "UTF-8"));
            jSONObject.put("up", GlobeVpnService.upBytes);
            jSONObject.put("down", GlobeVpnService.downBytes);
            long j = GlobeVpnService.connectedAt;
            long j2 = 0;
            if (j != 0) {
                j2 = (System.currentTimeMillis() - j) / 1000;
            }
            jSONObject.put("seconds", j2);
        } catch (Exception unused) {
        }
        return jSONObject.toString();
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void startPolling() {
        if (this.polling) {
            return;
        }
        this.polling = true;
        this.ui.postDelayed(new Runnable() { // from class: com.globe.vpn.MainActivity.4
            @Override // java.lang.Runnable
            public void run() {
                if (MainActivity.this.polling) {
                    MainActivity.this.callJs("window.__onVpnState && window.__onVpnState(" + JSONObject.quote(MainActivity.this.vpnStateJson()) + ")");
                    MainActivity.this.ui.postDelayed(this, 1000L);
                }
            }
        }, 700L);
    }

    @Override
    public void onRequestPermissionsResult(int code, String[] permissions, int[] results) {
        super.onRequestPermissionsResult(code, permissions, results);
        if (code == 4102) {
            boolean granted = results.length > 0
                    && results[0] == android.content.pm.PackageManager.PERMISSION_GRANTED;
            callJs("window.__onCameraPermission(" + granted + ")");
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    @Override
    public void onConfigurationChanged(android.content.res.Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        boolean dark = (newConfig.uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        callJs("window.__onSystemTheme && window.__onSystemTheme(" + dark + ")");
    }

    public void callJs(final String str) {
        runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.5
            @Override // java.lang.Runnable
            public void run() {
                if (MainActivity.this.web != null) {
                    MainActivity.this.web.evaluateJavascript(str, null);
                }
            }
        });
    }

    private void toast(final String str) {
        runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.6
            @Override // java.lang.Runnable
            public void run() {
                Toast.makeText(MainActivity.this, str, 0).show();
            }
        });
    }

    static String iconDataUrl(Drawable drawable) {
        Bitmap bitmap = Bitmap.createBitmap(48, 48, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        drawable.setBounds(0, 0, 48, 48);
        drawable.draw(canvas);
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 90, bytes);
        return "data:image/png;base64," + Base64.encodeToString(bytes.toByteArray(), Base64.NO_WRAP);
    }

    private class Bridge {
        @JavascriptInterface
        public boolean available() {
            return true;
        }

        private Bridge() {
        }

        @JavascriptInterface
        public void copy(String str) {
            ClipboardManager clipboardManager = (ClipboardManager) MainActivity.this.getSystemService("clipboard");
            if (clipboardManager == null) {
                return;
            }
            if (str == null) {
                str = "";
            }
            clipboardManager.setPrimaryClip(ClipData.newPlainText("smpl", str));
        }

        @JavascriptInterface
        public void readClipboard(String key) {
            String text = "";
            try {
                ClipboardManager manager = (ClipboardManager) MainActivity.this.getSystemService("clipboard");
                if (manager != null && manager.hasPrimaryClip() && manager.getPrimaryClip() != null
                        && manager.getPrimaryClip().getItemCount() > 0) {
                    CharSequence value = manager.getPrimaryClip().getItemAt(0).coerceToText(MainActivity.this);
                    if (value != null) {
                        text = value.toString();
                    }
                }
            } catch (Throwable ignored) {
            }
            MainActivity.this.callJs("window.__onClipboard && window.__onClipboard("
                    + JSONObject.quote(key == null ? "" : key) + ", "
                    + JSONObject.quote(text) + ")");
        }

        /** Виброотклик: 1 — слабый, 2 — средний, 3 — сильный. */
        @JavascriptInterface
        public void haptic(final int level) {
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.1
                @Override // java.lang.Runnable
                public void run() {
                    if (MainActivity.this.web == null) {
                        return;
                    }
                    if (level >= 3) {
                        MainActivity.this.web.performHapticFeedback(0, 2);
                    } else if (level == 2) {
                        MainActivity.this.web.performHapticFeedback(1, 2);
                    } else {
                        MainActivity.this.web.performHapticFeedback(1, 0);
                    }
                }
            });
        }

        /** Установленные приложения с запуском: [{"p": пакет, "n": название, "i": иконка PNG data-url}]. */
        @JavascriptInterface
        public String listApps() {
            try {
                PackageManager pm = getPackageManager();
                Intent launcher = new Intent(Intent.ACTION_MAIN);
                launcher.addCategory(Intent.CATEGORY_LAUNCHER);
                List<ResolveInfo> infos = pm.queryIntentActivities(launcher, 0);
                Set<String> seen = new HashSet<String>();
                JSONArray out = new JSONArray();
                for (ResolveInfo info : infos) {
                    String pkg = info.activityInfo.packageName;
                    if (pkg.equals(getPackageName()) || !seen.add(pkg)) {
                        continue;
                    }
                    JSONObject item = new JSONObject();
                    item.put("p", pkg);
                    item.put("n", String.valueOf(info.loadLabel(pm)));
                    item.put("i", iconDataUrl(info.loadIcon(pm)));
                    out.put(item);
                }
                return out.toString();
            } catch (Exception unused) {
                return "[]";
            }
        }

        /** Список приложений в обходе VPN (JSON-массив пакетов); применяется при следующем подключении. */
        /** Тема устройства: true — системная тёмная тема. */
        @JavascriptInterface
        public boolean systemDark() {
            int mode = getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK;
            return mode == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        }

        @JavascriptInterface
        public void setBypass(String json) {
            String value = json == null ? "[]" : json;
            getSharedPreferences("globe-vpn", 0).edit().putString("bypass", value).apply();
        }

        @JavascriptInterface
        public void setChrome(final String str, final boolean z) {
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.2
                @Override // java.lang.Runnable
                public void run() {
                    int parseColor;
                    try {
                        parseColor = Color.parseColor(str);
                    } catch (Exception unused) {
                        parseColor = Color.parseColor(z ? "#151613" : "#F2F0EA");
                    }
                    Window window = MainActivity.this.getWindow();
                    window.setStatusBarColor(parseColor);
                    window.setNavigationBarColor(parseColor);
                    MainActivity.this.setLightSystemBars(!z);
                }
            });
        }

        @JavascriptInterface
        public void toast(String str) {
            if (str == null) {
                str = "";
            }
            toast(str);
        }

        @JavascriptInterface
        public void ping(final String str) {
            MainActivity.this.pool.execute(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.3
                @Override // java.lang.Runnable
                public void run() {
                    JSONArray jSONArray = new JSONArray();
                    try {
                        String str2 = str;
                        if (str2 == null) {
                            str2 = "[]";
                        }
                        JSONArray jSONArray2 = new JSONArray(str2);
                        ArrayList arrayList = new ArrayList();
                        for (int i = 0; i < jSONArray2.length(); i++) {
                            JSONObject optJSONObject = jSONArray2.optJSONObject(i);
                            if (optJSONObject != null) {
                                final String optString = optJSONObject.optString("id", "");
                                final String optString2 = optJSONObject.optString("host", "");
                                final int optInt = optJSONObject.optInt("port", 443);
                                final int optTimeout = optJSONObject.optInt("timeout", 2500) > 0
                                        ? optJSONObject.optInt("timeout", 2500) : 2500;
                                if (!optString.isEmpty() && !optString2.isEmpty()) {
                                    arrayList.add(MainActivity.this.pool.submit(new Callable<JSONObject>() { // from class: com.globe.vpn.MainActivity.Bridge.3.1
                                        @Override // java.util.concurrent.Callable
                                        public JSONObject call() {
                                            JSONObject jSONObject = new JSONObject();
                                            try {
                                                jSONObject.put("id", optString);
                                                Socket socket = new Socket();
                                                try {
                                                    try {
                                                        long nanoTime = System.nanoTime();
                                                        socket.connect(new InetSocketAddress(optString2, optInt), optTimeout);
                                                        jSONObject.put("ms", (System.nanoTime() - nanoTime) / 1000000);
                                                        socket.close();
                                                    } catch (Throwable th) {
                                                        socket.close();
                                                        throw th;
                                                    }
                                                } catch (Exception unused) {
                                                }
                                            } catch (Exception unused2) {
                                                try {
                                                    jSONObject.put("id", optString);
                                                    jSONObject.put("ms", JSONObject.NULL);
                                                } catch (Exception ignored) {
                                                }
                                            }
                                            return jSONObject;
                                        }
                                    }));
                                }
                            }
                        }
                        Iterator it = arrayList.iterator();
                        while (it.hasNext()) {
                            try {
                                jSONArray.put(((Future) it.next()).get());
                            } catch (Exception unused) {
                            }
                        }
                    } catch (Exception unused2) {
                    }
                    MainActivity.this.callJs("window.__onLatency && window.__onLatency(" + JSONObject.quote(jSONArray.toString()) + ")");
                }
            });
        }

        @JavascriptInterface
        public void fetchText(final String key, final String url) {
            MainActivity.this.pool.execute(new Runnable() {
                @Override // java.lang.Runnable
                public void run() {
                    String body = "";
                    boolean ok = false;
                    // некоторые серверы подписок отдают HTML-витрину тому, кто не похож на VPN-клиент,
                    // поэтому перебираем несколько User-Agent и пропускаем HTML-ответы
                    String[] agents = {
                            "Happ/1.0",
                            "v2rayNG/1.8.5",
                            "GlobeVPN/1.0 (Android)"
                    };
                    for (String agent : agents) {
                        HttpURLConnection connection = null;
                        try {
                            connection = (HttpURLConnection) new java.net.URL(url).openConnection();
                            connection.setConnectTimeout(10000);
                            connection.setReadTimeout(12000);
                            connection.setInstanceFollowRedirects(true);
                            connection.setRequestProperty("User-Agent", agent);
                            connection.setRequestProperty("Accept", "*/*");
                            int code = connection.getResponseCode();
                            if (code >= 200 && code < 300) {
                                InputStream input = connection.getInputStream();
                                ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                                byte[] chunk = new byte[8192];
                                int count;
                                while ((count = input.read(chunk)) > 0) {
                                    buffer.write(chunk, 0, count);
                                }
                                input.close();
                                String text = buffer.toString("UTF-8");
                                if (looksLikeHtml(text)) {
                                    continue;
                                }
                                body = metaHeaders(connection) + text;
                                ok = true;
                                break;
                            }
                        } catch (Throwable ignored) {
                        } finally {
                            if (connection != null) {
                                connection.disconnect();
                            }
                        }
                    }
                    MainActivity.this.callJs("window.__onFetch && window.__onFetch("
                            + JSONObject.quote(key == null ? "" : key) + ","
                            + (ok ? "true" : "false") + ","
                            + JSONObject.quote(body) + ")");
                }
            });
        }

        private boolean looksLikeHtml(String text) {
            String head = text.length() > 4000 ? text.substring(0, 4000) : text;
            String lower = head.trim().toLowerCase(java.util.Locale.ROOT);
            return lower.startsWith("<!doctype") || lower.startsWith("<html") || lower.contains("<html");
        }

        // системное меню «Поделиться» с текстом подписки
        @JavascriptInterface
        public void shareText(final String text, final String title) {
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.share
                @Override // java.lang.Runnable
                public void run() {
                    Intent send = new Intent(Intent.ACTION_SEND);
                    send.setType("text/plain");
                    send.putExtra(Intent.EXTRA_TEXT, text == null ? "" : text);
                    if (title != null && !title.isEmpty()) {
                        send.putExtra(Intent.EXTRA_SUBJECT, title);
                    }
                    try {
                        MainActivity.this.startActivity(Intent.createChooser(send, "Поделиться подпиской"));
                    } catch (Exception ignored) {
                    }
                }
            });
        }

        @JavascriptInterface
        public void saveFile(final String str, String str2) {
            MainActivity mainActivity = MainActivity.this;
            if (str2 == null) {
                str2 = "";
            }
            mainActivity.pendingSaveText = str2;
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.5
                @Override // java.lang.Runnable
                public void run() {
                    String str3;
                    try {
                        Intent intent = new Intent("android.intent.action.CREATE_DOCUMENT");
                        intent.addCategory("android.intent.category.OPENABLE");
                        intent.setType("application/json");
                        String str4 = str;
                        if (str4 != null && !str4.isEmpty()) {
                            str3 = str;
                            intent.putExtra("android.intent.extra.TITLE", str3);
                            MainActivity.this.startActivityForResult(intent, MainActivity.REQ_SAVE);
                        }
                        str3 = "globe-vpn-backup.json";
                        intent.putExtra("android.intent.extra.TITLE", str3);
                        MainActivity.this.startActivityForResult(intent, MainActivity.REQ_SAVE);
                    } catch (Exception unused) {
                        Bridge.this.toast("Не удалось открыть сохранение файла");
                    }
                }
            });
        }

        @JavascriptInterface
        public void pickFile() {
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.6
                @Override // java.lang.Runnable
                public void run() {
                    try {
                        Intent intent = new Intent("android.intent.action.OPEN_DOCUMENT");
                        intent.addCategory("android.intent.category.OPENABLE");
                        intent.setType("*/*");
                        intent.putExtra("android.intent.extra.MIME_TYPES", new String[]{"application/json", "text/plain", "*/*"});
                        MainActivity.this.startActivityForResult(intent, MainActivity.REQ_OPEN);
                    } catch (Exception unused) {
                        Bridge.this.toast("Не удалось открыть выбор файла");
                    }
                }
            });
        }

        @JavascriptInterface
        public void connect(final String str, final String str2) {
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.7
                @Override // java.lang.Runnable
                public void run() {
                    try {
                        MainActivity.this.requestNotificationPermission();
                        Intent prepare = VpnService.prepare(MainActivity.this);
                        String str3 = "";
                        if (prepare != null) {
                            MainActivity.this.pendingVpnConfig = str;
                            MainActivity mainActivity = MainActivity.this;
                            String str4 = str2;
                            if (str4 != null) {
                                str3 = str4;
                            }
                            mainActivity.pendingVpnName = str3;
                            MainActivity.this.startActivityForResult(prepare, MainActivity.REQ_VPN);
                            return;
                        }
                        GlobeVpnService.state = GlobeVpnService.STATE_CONNECTING;
                        GlobeVpnService.lastError = "";
                        MainActivity.this.startVpn(str, str2);
                        MainActivity.this.startPolling();
                    } catch (Exception e) {
                        GlobeVpnService.state = GlobeVpnService.STATE_ERROR;
                        GlobeVpnService.lastError = String.valueOf(e.getMessage());
                    }
                }
            });
        }

        @JavascriptInterface
        public void disconnect() {
            MainActivity.this.runOnUiThread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.8
                @Override // java.lang.Runnable
                public void run() {
                    MainActivity.this.stopVpn();
                    GlobeVpnService.reset();
                }
            });
        }

        @JavascriptInterface
        public String vpnState() {
            return MainActivity.this.vpnStateJson();
        }

        @JavascriptInterface
        public void setNotice(String server, int pingMs) {
            GlobeVpnService.noticeServer = server == null ? "" : server;
            GlobeVpnService.noticePing = pingMs;
            GlobeVpnService service = GlobeVpnService.instance;
            if (service != null && GlobeVpnService.STATE_CONNECTED.equals(GlobeVpnService.state)) {
                service.refreshNotice();
            }
        }

        @JavascriptInterface
        public void requestCamera() {
            boolean granted = MainActivity.this.checkSelfPermission(android.Manifest.permission.CAMERA)
                    == android.content.pm.PackageManager.PERMISSION_GRANTED;
            if (!granted && Build.VERSION.SDK_INT >= 23) {
                MainActivity.this.runOnUiThread(new Runnable() {
                    @Override // java.lang.Runnable
                    public void run() {
                        MainActivity.this.requestPermissions(new String[]{android.Manifest.permission.CAMERA}, 4102);
                    }
                });
                return;
            }
            MainActivity.this.callJs("window.__onCameraPermission(" + granted + ")");
        }

        @JavascriptInterface
        public void locate(final String key) {
            MainActivity.this.pool.execute(new Runnable() {
                @Override // java.lang.Runnable
                public void run() {
                    String payload = "";
                    String[] endpoints = {
                        "http://ip-api.com/json/?fields=status,country,city,lat,lon",
                        "https://ipapi.co/json/"
                    };
                    for (int i = 0; i < endpoints.length && payload.isEmpty(); i++) {
                        HttpURLConnection connection = null;
                        try {
                            connection = (HttpURLConnection) new java.net.URL(endpoints[i]).openConnection();
                            connection.setConnectTimeout(6000);
                            connection.setReadTimeout(6000);
                            connection.setInstanceFollowRedirects(true);
                            connection.setRequestProperty("User-Agent", "GlobeVPN/1.0 (Android)");
                            connection.setRequestProperty("Accept", "application/json");
                            if (connection.getResponseCode() != 200) {
                                continue;
                            }
                            InputStream input = connection.getInputStream();
                            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                            byte[] chunk = new byte[4096];
                            int count;
                            while ((count = input.read(chunk)) > 0) {
                                buffer.write(chunk, 0, count);
                            }
                            input.close();
                            JSONObject raw = new JSONObject(buffer.toString("UTF-8"));
                            double lat = raw.optDouble("lat", Double.NaN);
                            double lng = raw.optDouble("lon", raw.optDouble("longitude", Double.NaN));
                            String city = raw.optString("city", "");
                            String country = raw.optString("country_name", raw.optString("country", ""));
                            if (Double.isNaN(lat) || Double.isNaN(lng)) {
                                continue;
                            }
                            JSONObject out = new JSONObject();
                            out.put("city", city);
                            out.put("country", country);
                            out.put("lat", lat);
                            out.put("lng", lng);
                            payload = out.toString();
                        } catch (Throwable ignored) {
                        } finally {
                            if (connection != null) {
                                connection.disconnect();
                            }
                        }
                    }
                    if (payload.isEmpty()) {
                        return;
                    }
                    MainActivity.this.callJs("window.__onLocate && window.__onLocate("
                            + JSONObject.quote(key == null ? "" : key) + ","
                            + JSONObject.quote(payload) + ")");
                }
            });
        }

        // Проверка работоспособности сервера полным конфигом; ответ уходит в window.__onProbe(key, ms)
        @JavascriptInterface
        public String networkKind() {
            return GlobeVpnService.networkKind(MainActivity.this);
        }

        @JavascriptInterface
        public void probe(final String key, final String configJson, final String url, final int timeoutMs) {
            final String probeUrl = (url == null || url.isEmpty()) ? "https://www.gstatic.com/generate_204" : url;
            final long[] result = {-1L};
            final Thread worker = new Thread(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.probe.1
                @Override // java.lang.Runnable
                public void run() {
                    try {
                        go.Seq.setContext(MainActivity.this.getApplicationContext());
                        libv2ray.Libv2ray.initCoreEnv(MainActivity.this.getFilesDir().getAbsolutePath(), "");
                        result[0] = libv2ray.Libv2ray.measureOutboundDelay(
                                GlobeVpnService.probeConfig(configJson), probeUrl);
                    } catch (Throwable error) {
                        result[0] = -1L;
                    }
                }
            }, "globe-probe");
            worker.setDaemon(true);
            MainActivity.this.pool.execute(new Runnable() { // from class: com.globe.vpn.MainActivity.Bridge.probe.2
                @Override // java.lang.Runnable
                public void run() {
                    long delay = -1L;
                    try {
                        worker.start();
                        worker.join(Math.max(1000L, timeoutMs) + 3000L);
                        delay = worker.isAlive() ? -1L : result[0];
                    } catch (InterruptedException error) {
                        delay = -1L;
                    }
                    MainActivity.this.callJs("window.__onProbe && window.__onProbe("
                            + JSONObject.quote(key == null ? "" : key) + "," + delay + ")");
                }
            });
        }

        @JavascriptInterface
        public void setAutopilot(final String json) {
            MainActivity.this.getSharedPreferences("globe-vpn", 0).edit()
                    .putString("autopilot", json == null ? "{}" : json).apply();
        }

        @JavascriptInterface
        public void measureDelay(final String key, final String outboundTag, final String url) {
            MainActivity.this.pool.execute(new Runnable() {
                @Override // java.lang.Runnable
                public void run() {
                    long delay;
                    try {
                        go.Seq.setContext(MainActivity.this.getApplicationContext());
                        libv2ray.Libv2ray.initCoreEnv(MainActivity.this.getFilesDir().getAbsolutePath(), "");
                        String probe = (url == null || url.isEmpty())
                                ? "https://www.google.com/generate_204" : url;
                        delay = libv2ray.Libv2ray.measureOutboundDelay(outboundTag, probe);
                    } catch (Throwable error) {
                        delay = -1;
                    }
                    MainActivity.this.callJs("window.__onDelay && window.__onDelay("
                            + JSONObject.quote(key == null ? "" : key) + "," + delay + ")");
                }
            });
        }

        @JavascriptInterface
        public void share(String str) {
            try {
                Intent intent = new Intent("android.intent.action.SEND");
                intent.setType("text/plain");
                intent.putExtra("android.intent.extra.TEXT", str);
                MainActivity.this.startActivity(Intent.createChooser(intent, "Поделиться"));
            } catch (Exception unused) {
                toast("Не удалось поделиться");
            }
        }
    }

    @Override // android.app.Activity
    protected void onActivityResult(int i, int i2, Intent intent) {
        super.onActivityResult(i, i2, intent);
        if (i2 != -1 || intent == null || intent.getData() == null) {
            return;
        }
        Uri data = intent.getData();
        if (i == REQ_SAVE) {
            try {
                OutputStream openOutputStream = getContentResolver().openOutputStream(data);
                if (openOutputStream != null) {
                    openOutputStream.write(this.pendingSaveText.getBytes("UTF-8"));
                    openOutputStream.close();
                }
            } catch (Exception unused) {
                toast("Не удалось сохранить файл");
            }
            this.pendingSaveText = "";
            return;
        }
        if (i != REQ_OPEN) {
            if (i == REQ_VPN) {
                if (i2 == -1 && this.pendingVpnConfig != null) {
                    GlobeVpnService.state = GlobeVpnService.STATE_CONNECTING;
                    GlobeVpnService.lastError = "";
                    startVpn(this.pendingVpnConfig, this.pendingVpnName);
                    startPolling();
                } else {
                    GlobeVpnService.state = GlobeVpnService.STATE_ERROR;
                    GlobeVpnService.lastError = "Разрешение VPN не выдано";
                }
                this.pendingVpnConfig = null;
                return;
            }
            return;
        }
        try {
            InputStream openInputStream = getContentResolver().openInputStream(data);
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            byte[] bArr = new byte[8192];
            while (openInputStream != null) {
                int read = openInputStream.read(bArr);
                if (read <= 0) {
                    break;
                } else {
                    byteArrayOutputStream.write(bArr, 0, read);
                }
            }
            if (openInputStream != null) {
                openInputStream.close();
            }
            callJs("window.__onImport && window.__onImport(" + JSONObject.quote(byteArrayOutputStream.toString("UTF-8")) + ")");
        } catch (Exception unused2) {
            toast("Не удалось прочитать файл");
        }
    }

    @Override // android.app.Activity
    public void onBackPressed() {
        WebView webView = this.web;
        if (webView == null) {
            super.onBackPressed();
        } else {
            webView.evaluateJavascript("(window.__nativeBack ? window.__nativeBack() : false)", new ValueCallback<String>() { // from class: com.globe.vpn.MainActivity.7
                @Override // android.webkit.ValueCallback
                public void onReceiveValue(String str) {
                    if (str == null || !str.contains("true")) {
                        long currentTimeMillis = System.currentTimeMillis();
                        if (currentTimeMillis - MainActivity.this.lastBackAt >= 2200) {
                            MainActivity.this.lastBackAt = currentTimeMillis;
                            Toast.makeText(MainActivity.this, "Нажмите «Назад» ещё раз, чтобы выйти", 0).show();
                        } else {
                            MainActivity.this.finish();
                        }
                    }
                }
            });
        }
    }

    @Override // android.app.Activity
    protected void onSaveInstanceState(Bundle bundle) {
        super.onSaveInstanceState(bundle);
        WebView webView = this.web;
        if (webView != null) {
            webView.saveState(bundle);
        }
    }

    @Override // android.app.Activity
    protected void onPause() {
        super.onPause();
        WebView webView = this.web;
        if (webView != null) {
            webView.onPause();
        }
    }

    @Override // android.app.Activity
    protected void onResume() {
        super.onResume();
        WebView webView = this.web;
        if (webView != null) {
            webView.onResume();
        }
        startPolling();
    }

    @Override // android.app.Activity
    protected void onStop() {
        super.onStop();
        this.polling = false;
    }

    @Override // android.app.Activity
    protected void onDestroy() {
        super.onDestroy();
        this.pool.shutdownNow();
        WebView webView = this.web;
        if (webView != null) {
            webView.loadUrl("about:blank");
            this.web.destroy();
            this.web = null;
        }
    }
}
