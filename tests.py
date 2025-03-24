import pytest

class TestBooksCollector:
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_long_name(self, collector):
        long_name = 'это слишком длинное название книги, которая не должна добавляться'
        collector.add_new_book(long_name)
        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize("book_name, expected_genre", [
        ('451 градус по Фаренгейту', 'Фантастика'),
        ('Война и мир', 'Детективы'),  # Использование существующего жанра
        ('Гарри Поттер', 'Фантастика'),  # Попробуем установить допустимый жанр
    ])
    def test_set_book_genre(self, collector, book_name, expected_genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, expected_genre)
        assert collector.get_book_genre(book_name) == expected_genre

    def test_set_book_wrong_genre(self, collector):
        collector.add_new_book('Гарри Поттер')  # Добавлено для корректного теста
        collector.set_book_genre('Гарри Поттер', 'Неверный Жанр')  # Попытка установить неверный жанр
        assert collector.get_book_genre('Гарри Поттер') == ''  # Утверждение для проверки, что жанр не установлен

    def test_get_book_genre(self, collector):
        collector.add_new_book('Война и мир')
        collector.set_book_genre('Война и мир', 'Детективы')
        assert collector.get_book_genre('Война и мир') == 'Детективы'

    @pytest.mark.parametrize("books, expected_genres", [
        (['1984', 'Война и мир'], {'1984': 'Фантастика', 'Война и мир': 'Детективы'}),
        (['Дешевый роман'], {'Дешевый роман': ''}),
        ([], {})
    ])
    def test_get_books_genre(self, collector, books, expected_genres):
        for book in books:
            collector.add_new_book(book)

        if '1984' in books:
            collector.set_book_genre('1984', 'Фантастика')
        if 'Война и мир' in books:
            collector.set_book_genre('Война и мир', 'Детективы')

        genres = collector.get_books_genre()
        assert genres == expected_genres

    def test_set_book_genre_invalid_book(self, collector):
        collector.set_book_genre('Неизвестная книга', 'Фантастика')
        assert collector.get_book_genre('Неизвестная книга') is None

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book('451 градус по Фаренгейту')
        collector.set_book_genre('451 градус по Фаренгейту', 'Фантастика')

        collector.add_new_book('Шагреневая кожа')
        collector.set_book_genre('Шагреневая кожа', 'Детективы')

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert fantasy_books == ['451 градус по Фаренгейту']

        horror_books = collector.get_books_with_specific_genre('Ужасы')
        assert horror_books == []

    def test_get_books_for_children(self, collector):
        collector.add_new_book('Приключения Петсона и Финдуса')
        collector.set_book_genre('Приключения Петсона и Финдуса', 'Мультфильмы')

        collector.add_new_book('Ужас на улице Вязов')
        collector.set_book_genre('Ужас на улице Вязов', 'Ужасы')

        children_books = collector.get_books_for_children()
        assert children_books == ['Приключения Петсона и Финдуса']

    def test_add_book_in_favorites(self, collector):
        collector.add_new_book('Муму')
        collector.add_book_in_favorites('Муму')

        assert len(collector.get_list_of_favorites_books()) == 1