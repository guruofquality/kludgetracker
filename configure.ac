AC_PREREQ(2.60)
AC_INIT(kludgetracker, 0)
AM_INIT_AUTOMAKE
##################################################
## Python Check
##################################################
AM_PATH_PYTHON([2.5])
AC_DEFUN([AC_PYTHON_MODULE], [
	AC_MSG_CHECKING([for python module $1])
	if ${PYTHON} -c "import $1" 2<&-; then
		AC_MSG_RESULT([found])
	else
		AC_MSG_RESULT([not found])
		AC_MSG_ERROR([Cannot import python module $1])
	fi
])
AC_PYTHON_MODULE([Cheetah])
##################################################
## Makefiles
##################################################
AC_CONFIG_FILES([ \
	Makefile \
	apps/Makefile \
	python/Makefile \
])
AC_OUTPUT
