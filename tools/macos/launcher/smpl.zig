extern "c" fn _NSGetExecutablePath(buf: [*]u8, bufsize: *u32) c_int;
extern "c" fn execv(path: [*:0]const u8, argv: [*:null]const ?[*:0]const u8) c_int;

const suffix = "/../Resources/index.html";

pub fn main() void {
    var buf: [4096]u8 = undefined;
    var size: u32 = buf.len;
    if (_NSGetExecutablePath(&buf, &size) != 0) return;
    // длина пути до последнего '/': .../smpl.app/Contents/MacOS
    var n: usize = 0;
    var i: usize = 0;
    while (i < buf.len and buf[i] != 0) : (i += 1) {
        if (buf[i] == '/') n = i;
    }
    if (n == 0 or n + suffix.len + 1 > buf.len) return;
    var out: [4096]u8 = undefined;
    var k: usize = 0;
    while (k < n) : (k += 1) out[k] = buf[k];
    var j: usize = 0;
    while (j < suffix.len) : (j += 1) out[n + j] = suffix[j];
    out[n + suffix.len] = 0;
    const page: [*:0]const u8 = @ptrCast(&out);
    const argv = [_:null]?[*:0]const u8{ "/usr/bin/open", page, null };
    _ = execv("/usr/bin/open", &argv);
}
