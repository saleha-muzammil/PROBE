#ifdef __APPLE__
typedef int (*__ftw_func_t)(const char *fpath, const struct stat *sb, int typeflag);
typedef int (*__nftw_func_t)(const char *fpath, const struct stat *sb, int typeflag, struct FTW *ftwbuf);
#endif

static FILE * (*unwrapped_fopen)(const char *filename, const char *opentype);
static FILE * (*unwrapped_freopen)(const char *filename, const char *opentype, FILE *stream);
static int (*unwrapped_fclose)(FILE *stream);
static int (*unwrapped_fcloseall)();
static int (*unwrapped_openat)(int dirfd, const char *filename, int flags, ...);
static int (*unwrapped_open)(const char *filename, int flags, ...);
static int (*unwrapped_creat)(const char *filename, mode_t mode);
static int (*unwrapped_close)(int filedes);

#ifdef __linux__
static int (*unwrapped_close_range)(unsigned int lowfd, unsigned int maxfd, int flags);
#endif

static void (*unwrapped_closefrom)(int lowfd);
static int (*unwrapped_dup)(int old);
static int (*unwrapped_dup2)(int old, int new);

#ifdef __linux__
static int (*unwrapped_dup3)(int old, int new, int flags);
#endif

static int (*unwrapped_fcntl)(int filedes, int command, ...);
static int (*unwrapped_chdir)(const char *filename);
static int (*unwrapped_fchdir)(int filedes);
static DIR * (*unwrapped_opendir)(const char *dirname);
static DIR * (*unwrapped_fdopendir)(int fd);
static struct dirent * (*unwrapped_readdir)(DIR *dirstream);
static int (*unwrapped_readdir_r)(DIR *dirstream, struct dirent *entry, struct dirent **result);

#ifdef __linux__
static struct dirent64 * (*unwrapped_readdir64)(DIR *dirstream);
static int (*unwrapped_readdir64_r)(DIR *dirstream, struct dirent64 *entry, struct dirent64 **result);
#endif

static int (*unwrapped_closedir)(DIR *dirstream);
static void (*unwrapped_rewinddir)(DIR *dirstream);
static long int (*unwrapped_telldir)(DIR *dirstream);
static void (*unwrapped_seekdir)(DIR *dirstream, long int pos);
static int (*unwrapped_scandir)(const char *dir, struct dirent ***namelist, int (*selector)(const struct dirent *), int (*cmp)(const struct dirent **, const struct dirent **));

#ifdef __linux__
static int (*unwrapped_scandir64)(const char *dir, struct dirent64 ***namelist, int (*selector)(const struct dirent64 *), int (*cmp)(const struct dirent64 **, const struct dirent64 **));
static int (*unwrapped_scandirat)(int dirfd, const char * restrict dirp, struct dirent *** restrict namelist, int (*filter)(const struct dirent *), int (*compar)(const struct dirent **, const struct dirent **));
static ssize_t (*unwrapped_getdents64)(int fd, void *buffer, size_t length);
#endif

static int (*unwrapped_ftw)(const char *filename, __ftw_func_t func, int descriptors);

#ifdef __linux__
static int (*unwrapped_ftw64)(const char *filename, __ftw64_func_t func, int descriptors);
#endif

static int (*unwrapped_nftw)(const char *filename, __nftw_func_t func, int descriptors, int flag);

#ifdef __linux__
static int (*unwrapped_nftw64)(const char *filename, __nftw64_func_t func, int descriptors, int flag);
#endif

static int (*unwrapped_link)(const char *oldname, const char *newname);
static int (*unwrapped_linkat)(int oldfd, const char *oldname, int newfd, const char *newname, int flags);
static int (*unwrapped_symlink)(const char *oldname, const char *newname);
static int (*unwrapped_symlinkat)(const char *target, int newdirfd, const char *linkpath);
static ssize_t (*unwrapped_readlink)(const char *filename, char *buffer, size_t size);
static ssize_t (*unwrapped_readlinkat)(int dirfd, const char *filename, char *buffer, size_t size);

#ifdef __linux__
static char * (*unwrapped_canonicalize_file_name)(const char *name);
#endif

static char * (*unwrapped_realpath)(const char * restrict name, char * restrict resolved);
static int (*unwrapped_unlink)(const char *filename);
static int (*unwrapped_rmdir)(const char *filename);
static int (*unwrapped_remove)(const char *filename);
static int (*unwrapped_rename)(const char *oldname, const char *newname);
static int (*unwrapped_mkdir)(const char *filename, mode_t mode);
static int (*unwrapped_mkdirat)(int dirfd, const char *pathname, mode_t mode);
static int (*unwrapped_stat)(const char *filename, struct stat *buf);

#ifdef __linux__
static int (*unwrapped_stat64)(const char *filename, struct stat64 *buf);
#endif

static int (*unwrapped_fstat)(int filedes, struct stat *buf);

#ifdef __linux__
static int (*unwrapped_fstat64)(int filedes, struct stat64 * restrict buf);
#endif

static int (*unwrapped_lstat)(const char *filename, struct stat *buf);

#ifdef __linux__
static int (*unwrapped_lstat64)(const char *filename, struct stat64 *buf);
static int (*unwrapped_statx)(int dirfd, const char * restrict pathname, int flags, unsigned int mask, struct statx * restrict statxbuf);
#endif

static int (*unwrapped_fstatat)(int dirfd, const char * restrict pathname, struct stat * restrict buf, int flags);

#ifdef __linux__
static int (*unwrapped_fstatat64)(int fd, const char * restrict file, struct stat64 * restrict buf, int flags);
#endif

static int (*unwrapped_chown)(const char *filename, uid_t owner, gid_t group);
static int (*unwrapped_fchown)(int filedes, uid_t owner, gid_t group);
static int (*unwrapped_lchown)(const char *pathname, uid_t owner, gid_t group);
static int (*unwrapped_fchownat)(int dirfd, const char *pathname, uid_t owner, gid_t group, int flags);
static int (*unwrapped_chmod)(const char *filename, mode_t mode);
static int (*unwrapped_fchmod)(int filedes, mode_t mode);
static int (*unwrapped_fchmodat)(int dirfd, const char *pathname, mode_t mode, int flags);
static int (*unwrapped_access)(const char *filename, int how);
static int (*unwrapped_faccessat)(int dirfd, const char *pathname, int mode, int flags);
static int (*unwrapped_utime)(const char *filename, const struct utimbuf *times);
static int (*unwrapped_utimes)(const char *filename, const struct timeval tvp[2]);
static int (*unwrapped_lutimes)(const char *filename, const struct timeval tvp[2]);
static int (*unwrapped_futimes)(int fd, const struct timeval tvp[2]);
static int (*unwrapped_truncate)(const char *filename, off_t length);

#ifdef __linux__
static int (*unwrapped_truncate64)(const char *name, off64_t length);
#endif

static int (*unwrapped_ftruncate)(int fd, off_t length);

#ifdef __linux__
static int (*unwrapped_ftruncate64)(int id, off64_t length);
#endif

static int (*unwrapped_mknod)(const char *filename, mode_t mode, dev_t dev);
static FILE * (*unwrapped_tmpfile)();

#ifdef __linux__
static FILE * (*unwrapped_tmpfile64)();
#endif

static char * (*unwrapped_tmpnam)(char *result);
static char * (*unwrapped_tmpnam_r)(char *result);
static char * (*unwrapped_tempnam)(const char *dir, const char *prefix);
static char * (*unwrapped_mktemp)(char *template);
static int (*unwrapped_mkstemp)(char *template);
static char * (*unwrapped_mkdtemp)(char *template);
static int (*unwrapped_execv)(const char *filename, char * const argv[]);
static int (*unwrapped_execl)(const char *filename, const char *arg0, ...);
static int (*unwrapped_execve)(const char *filename, char * const argv[], char * const env[]);
static int (*unwrapped_fexecve)(int fd, char * const argv[], char * const env[]);
static int (*unwrapped_execle)(const char *filename, const char *arg0, ...);
static int (*unwrapped_execvp)(const char *filename, char * const argv[]);
static int (*unwrapped_execlp)(const char *filename, const char *arg0, ...);

#ifdef __linux__
static int (*unwrapped_execvpe)(const char *filename, char * const argv[], char * const envp[]);
#endif

static pid_t (*unwrapped_fork)();

#ifdef __linux__
static pid_t (*unwrapped__Fork)();
#endif

static pid_t (*unwrapped_vfork)();

#ifdef __linux__
static int (*unwrapped_clone)(fn_ptr_int_void_ptr fn, void *stack, int flags, void *arg, ...);
#endif

static pid_t (*unwrapped_waitpid)(pid_t pid, int *status_ptr, int options);
static pid_t (*unwrapped_wait)(int *status_ptr);
static pid_t (*unwrapped_wait4)(pid_t pid, int *status_ptr, int options, struct rusage *usage);
static pid_t (*unwrapped_wait3)(int *status_ptr, int options, struct rusage *usage);
static int (*unwrapped_waitid)(idtype_t idtype, id_t id, siginfo_t *infop, int options);

#ifdef __linux__
static int (*unwrapped_thrd_create)(thrd_t *thr, thrd_start_t func, void *arg);
static int (*unwrapped_thrd_join)(thrd_t thr, int *res);
#endif

static int (*unwrapped_pthread_create)(pthread_t * restrict thread, const pthread_attr_t * restrict attr, void *(*start_routine)(void *), void * restrict arg);
static int (*unwrapped_pthread_join)(pthread_t thread, void **retval);

#ifdef __linux__
static FILE * (*unwrapped_fopen64)(const char *filename, const char *opentype);
static FILE * (*unwrapped_freopen64)(const char *filename, const char *opentype, FILE *stream);
static int (*unwrapped_openat64)(int dirfd, const char *filename, int flags, ...);
static int (*unwrapped_open64)(const char *filename, int flags, ...);
static int (*unwrapped_create64)(const char *filename, mode_t mode);
#endif
