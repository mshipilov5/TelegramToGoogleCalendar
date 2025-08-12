

import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():

    loader = unittest.TestLoader()

    test_files = [
        'test_config_loader',
        'test_mistral_ai', 
        'test_gcalendar',
        'test_telegram',
    ]


    suite = unittest.TestSuite()
    
    for test_file in test_files:
        try:
            module_tests = loader.loadTestsFromName(f'tests.{test_file}')
            suite.addTests(module_tests)
            print(f"✅ Загружены тесты из {test_file}.py")
        except Exception as e:
            print(f"❌ Ошибка загрузки тестов из {test_file}.py: {e}")

    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True
    )
    
    print("\n🚀 Запуск тестов...")
    print("=" * 50)

    result = runner.run(suite)
    
    print("=" * 50)
    print(f"📊 Результаты тестирования:")
    print(f"   Тестов запущено: {result.testsRun}")
    print(f"   Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Ошибок: {len(result.errors)}")
    print(f"   Провалов: {len(result.failures)}")
    
    if result.failures:
        print(f"\n❌ Проваленные тесты:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n💥 Тесты с ошибками:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")

    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_name):
    loader = unittest.TestLoader()
    
    try:
        module_tests = loader.loadTestsFromName(f'tests.{test_name}')
        
        runner = unittest.TextTestRunner(verbosity=2)
        print(f"🚀 Запуск тестов из {test_name}.py...")
        
        result = runner.run(module_tests)
        return 0 if result.wasSuccessful() else 1
        
    except Exception as e:
        print(f"❌ Ошибка загрузки тестов из {test_name}.py: {e}")
        return 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
