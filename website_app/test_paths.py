import os
print(__file__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#print(basedir)
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#filename = os.path.basename(__file__)
#filename = __file__.replace(BASE_DIR, '').replace('\\..', '').replace('\\', '')
#print(filename)

#Return a normalized absolutized version of the pathname path. On most platforms, this is equivalent to calling the function normpath() as follows: normpath(join(os.getcwd(), path)).
print('1.abspath',os.path.abspath(__file__))

# #Return the base name of pathname path. This is the second element of the pair returned by passing path to the function split(). Note that the result of this function is different from the Unix basename program; where basename for '/foo/bar/' returns 'bar', the basename() function returns an empty string ('').
print('2.basename',os.path.basename(__file__))
print('3.dirname',os.path.dirname(__file__))

# #Return the longest path prefix (taken character-by-character) that is a prefix of all paths in list. If list is empty, return the empty string (''). Note that this may return invalid paths because it works a character at a time.
# os.path.commonprefix(list)


# #Return True if path refers to an existing path. Returns False for broken symbolic links. On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists.
# os.path.exists(path)

# #Return True if path refers to an existing path. Returns True for broken symbolic links. Equivalent to exists() on platforms lacking os.lstat().
# os.path.lexists(path)

# #On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user’s home directory.
print('4.expanduser',os.path.expanduser(__file__))

# #Return the argument with environment variables expanded. Substrings of the form $name or ${name} are replaced by the value of environment variable name. Malformed variable names and references to non-existing variables are left unchanged.
# #On Windows, %name% expansions are supported in addition to $name and ${name}.
# os.path.expandvars(path)


# #Return the time of last access of path. The return value is a number giving the number of seconds since the epoch (see the time module). Raise os.error if the file does not exist or is inaccessible.
# os.path.getatime(path)

# #Return the time of last modification of path. The return value is a number giving the number of seconds since the epoch (see the time module). Raise os.error if the file does not exist or is inaccessible.
# os.path.getmtime(path)

# #Return the system’s ctime which, on some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time for path. The return value is a number giving the number of seconds since the epoch (see the time module). Raise os.error if the file does not exist or is inaccessible.
# os.path.getctime(path)

# #Return True if path is an absolute pathname. On Unix, that means it begins with a slash, on Windows that it begins with a (back)slash after chopping off a potential drive letter.
# os.path.isabs(path)

# #Return True if path is an existing regular file. This follows symbolic links, so both islink() and isfile() can be true for the same path.
# os.path.isfile(path)

# #Return True if path is an existing directory. This follows symbolic links, so both islink() and isdir() can be true for the same path.
# os.path.isdir(path)

# Return True if path refers to a directory entry that is a symbolic link. Always False if symbolic links are not supported by the Python runtime.
# os.path.islink(path)


# #Join one or more path components intelligently. The return value is the concatenation of path and any members of *paths with exactly one directory separator (os.sep) following each non-empty part except the last, meaning that the result will only end in a separator if the last part is empty. If a component is an absolute path, all previous components are thrown away and joining continues from the absolute path component.
# #On Windows, the drive letter is not reset when an absolute path component (e.g., r'\foo') is encountered. If a component contains a drive letter, all previous components are thrown away and the drive letter is reset. Note that since there is a current directory for each drive, os.path.join("c:", "foo") represents a path relative to the current directory on drive C: (c:foo), not c:\foo.
# os.path.join(path, *paths)


# os.path.normcase(path)
# Normalize the case of a pathname. On Unix and Mac OS X, this returns the path unchanged; on case-insensitive filesystems, it converts the path to lowercase. On Windows, it also converts forward slashes to backward slashes.

# os.path.normpath(path)
# Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B. This string manipulation may change the meaning of a path that contains symbolic links. On Windows, it converts forward slashes to backward slashes. To normalize case, use normcase().

# os.path.realpath(path)
# Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).

# os.path.relpath(path[, start])
# Return a relative filepath to path either from the current directory or from an optional start directory. This is a path computation: the filesystem is not accessed to confirm the existence or nature of path or start.


# os.path.samefile(path1, path2)
# Return True if both pathname arguments refer to the same file or directory (as indicated by device number and i-node number). Raise an exception if an os.stat() call on either pathname fails.

# os.path.sameopenfile(fp1, fp2)
# Return True if the file descriptors fp1 and fp2 refer to the same file.

# os.path.samestat(stat1, stat2)
# Return True if the stat tuples stat1 and stat2 refer to the same file. These structures may have been returned by os.fstat(), os.lstat(), or os.stat(). This function implements the underlying comparison used by samefile() and sameopenfile().

# Availability: Unix.

# os.path.split(path)
# Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty. Trailing slashes are stripped from head unless it is the root (one or more slashes only). In all cases, join(head, tail) returns a path to the same location as path (but the strings may differ). Also see the functions dirname() and basename().

# os.path.splitdrive(path)
# Split the pathname path into a pair (drive, tail) where drive is either a drive specification or the empty string. On systems which do not use drive specifications, drive will always be the empty string. In all cases, drive + tail will be the same as path.

# New in version 1.3.

# os.path.splitext(path)
# Split the pathname path into a pair (root, ext) such that root + ext == path, and ext is empty or begins with a period and contains at most one period. Leading periods on the basename are ignored; splitext('.cshrc') returns ('.cshrc', '').

