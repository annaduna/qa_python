import pytest

class TestBooksCollector:
    def test_add_new_book_add_two_books(self,collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_long_name(self, collector):
        """Тест на добавление книги с длинным названием."""
        long_name = 'это слишком длинное название книги, которая не должна добавляться'
        collector.add_new_book(long_name)
        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize("book_name, expected_genre", [
        ('451 градус по Фаренгейту', 'Фантастика'),
        ('Война и мир', 'Исторический роман'),
    ])
    def test_set_book_genre(self, collector, book_name, expected_genre):
        """Тест на установку жанра книги с параметризацией."""
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, expected_genre)
        assert collector.get_book_genre(book_name) == expected_genre

    def test_set_book_wrong_genre(self,collector):
        collector.set_book_genre('Гарри Поттер', 'Неверный Жанр')
        assert collector.get_book_genre('Гарри Поттер') == 'Фантастика'

    def test_get_book_genre(self,collector):
        collector.add_new_book('Война и мир')
        collector.set_book_genre('Война и мир', 'Детективы')

        assert collector.get_book_genre('Война и мир') == 'Детективы'

    @pytest.mark.parametrize("books, expected_genres", [
        (['1984', 'Война и мир'], {'1984': 'Фантастика', 'Война и мир': 'Исторический роман'}),
        (['Дешевый роман'], {'Дешевый роман': ''}),  # Проверка книги без жанра
        ([], {})  # Проверка на пустой список книг
    ])
    def test_get_books_genre(self, collector, books, expected_genres):
        """Параметризованный тест на получение словаря всех книг с жанрами."""
        for book in books:
            collector.add_new_book(book)

        # Присваиваем жанры для тестовых книг
        if '1984' in books:
            collector.set_book_genre('1984', 'Фантастика')
        if 'Война и мир' in books:
            collector.set_book_genre('Война и мир', 'Исторический роман')

        genres = collector.get_books_genre()
        assert genres == expected_genres

    def test_set_book_genre_invalid_book(self, collector):
        """Тест на установку жанра для несуществующей книги."""
        collector.set_book_genre('Неизвестная книга', 'Фантастика')
        assert collector.get_book_genre('Неизвестная книга') is None  # Жанр не должен устанавливаться

    def test_get_books_with_specific_genre(self, collector):
        """Тест на получение книг с определённым жанром."""
        collector.add_new_book('451 градус по Фаренгейту')
        collector.set_book_genre('451 градус по Фаренгейту', 'Фантастика')

        collector.add_new_book('Шагреневая кожа')
        collector.set_book_genre('Шагреневая кожа', 'Детективы')

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert fantasy_books == ['451 градус по Фаренгейту']

        # Проверяем, что нет книг с неправильным жанром
        horror_books = collector.get_books_with_specific_genre('Ужасы')
        assert horror_books == []

    def test_get_books_for_children(self, collector):
        """Тест на получение книг для детей."""
        collector.add_new_book('Приключения Петсона и Финдуса')
        collector.set_book_genre('Приключения Петсона и Финдуса', 'Мультфильмы')  # Подходит детям

        collector.add_new_book('Ужас на улице Вязов')
        collector.set_book_genre('Ужас на улице Вязов', 'Ужасы')  # Не подходит детям

        children_books = collector.get_books_for_children()
        assert children_books == ['Приключения Петсона и Финдуса']  # Ужасы не должны быть в списке

    def test_add_book_in_favorites(self, collector):
        """Тест на добавление книги в избранное."""
        collector.add_new_book('Муму')
        collector.add_book_in_favorites('Муму')

        assert len(collector.get_list_of_favorites_books()) == 1


    def test_add_book_in_favorites_again(self, collector):
     collector.add_book_in_favorites('Муму')
     assert len(collector.get_list_of_favorites_books()) == 1  # Должно остаться 1 книга

    def test_delete_book_from_favorites(self, collector):
        """Тест на удаление книги из избранного."""
        collector.add_new_book('Собака Баскервилей')
        collector.add_book_in_favorites('Собака Баскервилей')

        collector.delete_book_from_favorites('Собака Баскервилей')
        assert len(collector.get_list_of_favorites_books()) == 0

    @pytest.mark.parametrize("books_to_add, favorites_to_add, expected_favorites", [
        (['Муму', 'Собака Баскервилей'], ['Муму'], ['Муму']),
        (['Шинель'], ['Шинель'], ['Шинель']),
        (['Кот в сапогах'], [], []),  # Проверка без добавления в избранное
        ([], [], []),  # Пустой набор книг
    ])
    def test_get_list_of_favorites_books(self, collector, books_to_add, favorites_to_add, expected_favorites):
        """Параметризованный тест на получение списка избранных книг."""
        for book in books_to_add:
            collector.add_new_book(book)

        for favorite in favorites_to_add:
            collector.add_book_in_favorites(favorite)

        favorites = collector.get_list_of_favorites_books()
        assert favorites == expected_favorites



