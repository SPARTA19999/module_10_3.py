import threading
import time
import random


class Bank:
    def __init__(self):
        self.balance = 0  # Изначальный баланс
        self.lock = threading.Lock()  # Объект Lock для синхронизации

    def deposit(self):
        for _ in range(100):
            amount = random.randint(50, 500)
            self.balance += amount
            print(f"Пополнение: {amount}. Баланс: {self.balance}")

            # Если баланс >= 500 и замок заблокирован, разблокировать его
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

            time.sleep(0.001)  # Имитируем скорость выполнения пополнения

    def take(self):
        for _ in range(100):
            amount = random.randint(50, 500)
            print(f"Запрос на {amount}")

            if amount <= self.balance:
                self.balance -= amount
                print(f"Снятие: {amount}. Баланс: {self.balance}")
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()  # Блокируем поток при недостаточном балансе

            time.sleep(0.001)  # Имитируем скорость выполнения снятия


def main():
    # Создание объекта Bank
    bk = Bank()

    # Создание потоков для методов deposit и take
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    # Запуск потоков
    th1.start()
    th2.start()

    # Ожидание завершения потоков
    th1.join()
    th2.join()

    # Вывод итогового баланса
    print(f"Итоговый баланс: {bk.balance}")


if __name__ == "__main__":
    main()
