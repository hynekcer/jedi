import logging
import traceback
import sys
logging.warn('\nstart conftest %s' % [k for k, v in sorted(sys.modules.items()) if v and 'jedi' in k])
logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))

import os
import shutil
import tempfile

import pytest

from . import test_dir

def pytest_addoption(parser):

    logging.warn('\nstart pytest_addoption %s' % [k for k, v in sorted(sys.modules.items()) if v and 'jedi' in k])
    logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))
    parser.addoption(
        "--integration-case-dir",
        default=os.path.join(test_dir, 'completion'),
        help="Directory in which integration test case files locate.")
    parser.addoption(
        "--refactor-case-dir",
        default=os.path.join(test_dir, 'refactor'),
        help="Directory in which refactoring test case files locate.")
    parser.addoption(
        "--test-files", "-T", default=[], action='append',
        help=(
            "Specify test files using FILE_NAME[:LINE[,LINE[,...]]]. "
            "For example: -T generators.py:10,13,19. "
            "Note that you can use -m to specify the test case by id."))
    parser.addoption(
        "--thirdparty", action='store_true',
        help="Include integration tests that requires third party modules.")
    logging.warn('end pytest_addoption %s\n' % [k for k, v in sorted(sys.modules.items()) if v and 'jedi' in k])


def parse_test_files_option(opt):
    """
    Parse option passed to --test-files into a key-value pair.

    >>> parse_test_files_option('generators.py:10,13,19')
    ('generators.py', [10, 13, 19])
    """
    logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))
    from . import base, run, refactor
    opt = str(opt)
    if ':' in opt:
        (f_name, rest) = opt.split(':', 1)
        return (f_name, list(map(int, rest.split(','))))
    else:
        return (opt, [])


def pytest_generate_tests(metafunc):
    """
    :type metafunc: _pytest.python.Metafunc
    """
    logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))
    from . import base, run, refactor
    test_files = dict(map(parse_test_files_option,
                          metafunc.config.option.test_files))
    if 'case' in metafunc.fixturenames:
        base_dir = metafunc.config.option.integration_case_dir
        thirdparty = metafunc.config.option.thirdparty
        cases = list(run.collect_dir_tests(base_dir, test_files))
        if thirdparty:
            cases.extend(run.collect_dir_tests(
                os.path.join(base_dir, 'thirdparty'), test_files, True))
        metafunc.parametrize('case', cases)
    if 'refactor_case' in metafunc.fixturenames:
        base_dir = metafunc.config.option.refactor_case_dir
        metafunc.parametrize(
            'refactor_case',
            refactor.collect_dir_tests(base_dir, test_files))


@pytest.fixture()
def isolated_jedi_cache(monkeypatch, tmpdir):
    """
    Set `jedi.settings.cache_directory` to a temporary directory during test.

    Same as `clean_jedi_cache`, but create the temporary directory for
    each test case (scope='function').
    """
    logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))
    from . import base, run, refactor
    settings = base.jedi.settings
    monkeypatch.setattr(settings, 'cache_directory', str(tmpdir))


@pytest.fixture(scope='session')
def clean_jedi_cache(request):
    """
    Set `jedi.settings.cache_directory` to a temporary directory during test.

    Note that you can't use built-in `tmpdir` and `monkeypatch`
    fixture here because their scope is 'function', which is not used
    in 'session' scope fixture.

    This fixture is activated in ../pytest.ini.
    """
    logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))
    from . import base, run, refactor
    settings = base.jedi.settings
    old = settings.cache_directory
    tmp = tempfile.mkdtemp(prefix='jedi-test-')
    settings.cache_directory = tmp

    @request.addfinalizer
    def restore():
        settings.cache_directory = old
        shutil.rmtree(tmp)

logging.warn('end conftest %s\n' % [k for k, v in sorted(sys.modules.items()) if v and 'jedi' in k])
