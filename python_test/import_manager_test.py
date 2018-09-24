import os
import subprocess
import sys

from unittest import TestCase
from mock import patch
from python.import_manager import TaskService
from python_test.import_task import redis, hello_world, ENV_BROKER_URL


def setUpModule():
    print '\nRunning tests for Python scripts'
    print '======================================================================'


def tearDownModule():
    print '\nEnd tests for Python scripts'
    print '======================================================================'


class TaskServiceTest(TestCase):

    worker_process = None

    @classmethod
    def setUpClass(cls):
        cls.start_worker()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.shutdown_worker()
        finally:
            print '\nShutting down redis server'
            redis.shutdown()

    @classmethod
    def start_worker(cls):
        print('Starting celery worker...')
        cmd = 'celery worker -A python_test.import_task -l info -b ' + os.getenv(ENV_BROKER_URL).__str__() + ' -n test'
        cls.worker_process = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
        cls.worker_process = cls.worker_process
        print 'Celery worker pid: ' + cls.worker_process.pid.__str__()

        """ Wait until the worker is ready """
        while True:
            out = cls.worker_process.stderr.readline()
            if (out == '' and cls.worker_process.poll() is not None) or out.endswith('ready.\n'):
                if out.endswith('ready.\n'):
                    sys.stdout.write(out)
                    sys.stdout.flush()

                print 'Worker started successfully\n'
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()

    @classmethod
    def shutdown_worker(cls):
        print '\nStopping celery worker'
        cls.worker_process.terminate()


    """ ===================== Actual TaskService Tests ===================== """

    #def test_get_active_tasks_should_return_nothing_if_no_active_tasks(self):
    #    self.assertListEqual([], TaskService.get_all_tasks())

    def test_get_all_tasks_should_return_all_active_tasks(self):
        ret = hello_world.apply_async(countdown=2)
        print 'Task Id: '+ret.task_id
        active_tasks = TaskService.get_all_tasks()
        self.assertEquals(1, active_tasks.__len__())


class ImportManagerTest(TestCase):

    @patch.object(TaskService, 'get_all_tasks')
    def test(self, get_all_tasks):
        print 'Running test'
        self.assertTrue(True)
        get_all_tasks.return_value = None
        self.assertIsNone(get_all_tasks())
