#!/bin/bash
set -e

function help_text() {
    cat <<EOF
    Usage: $0 [ -t|--test-suite TEST_SUITE ]
        --test-suite	Test suite (unit/integration)
EOF
    exit 1
}

while [[ $# -gt 0 ]]; do
    arg=$1
    case $arg in
    -h | --help)
        help_text
        ;;
    -t | --test-suite)
        export TEST_SUITE="$2"
        shift
        shift
        ;;
    *)
        echo "ERROR: Unrecognised option: ${arg}"
        help_text
        exit 1
        ;;
    esac
done

echo "**********************"
if [ -z "${SRC_DIR}" ]; then
    SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
fi

PY_EXE=`which python`
SOURCE_DIR=`${PY_EXE} -c "import app; print(list(app.__path__)[0])"`
VERSION=`${PY_EXE} -c "import app; print(app.__version__)"`

echo "SRC_DIR: $SRC_DIR"
echo "Python: $PY_EXE"
echo "Python Path: $PYTHONPATH"
echo "Path: $PATH"
echo "Version: $VERSION"

echo "********************** pytest"
export COVERAGE_RCFILE=$SRC_DIR/.conda/.coveragerc
${PY_EXE} -m coverage run --source ${SOURCE_DIR} -m pytest --junitxml=/tmp/test-reports/pytest-junit.xml tests/$TEST_SUITE
${PY_EXE} -m coverage html
${PY_EXE} -m coverage json
${PY_EXE} -m coverage report
