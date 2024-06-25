#!/usr/bin/python3

import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
from models import storage


class TestHBNBCommand(unittest.TestCase):

    __list = ["User", "City", "Place", "BaseModel",
              "State", "Amenity", "Review"]

    def test_costum_prompt(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

    def test_quit_exits(self):
        self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_help_quit(self):
        txt = "Quits console"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("help quit")
            self.assertEqual(txt, output.getvalue().strip())

    def test_help_EOF(self):
        txt = "Exits console"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual(txt, output.getvalue().strip())

    def test_help_create(self):
        txt = ("Create a new instance of a class.\n        "
               "Usage: create <class_name>")
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("help create")
            self.assertEqual(txt, output.getvalue().strip())

    def test_create_missing_class(self):
        errorString = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create")
            self.assertEqual(errorString, output.getvalue().strip())

    def test_create_invalid_class(self):
        errorString = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual(errorString, output.getvalue().strip())

    def test_create(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            Key = f"BaseModel.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            Key = f"User.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            Key = f"State.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            Key = f"City.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            Key = f"Amenity.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            Key = f"Place.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            Key = f"Review.{output.getvalue().strip()}"
            self.assertIn(Key, storage.all().keys())

    def test_create_with_attributes(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create User name="John_Doe" age=30 height=5.9')
            instance_id = output.getvalue().strip()
            key = f"User.{instance_id}"
            self.assertIn(key, storage.all().keys())
            
            new_instance = storage.all()[key]
            self.assertEqual(new_instance.name, "John Doe")
            self.assertEqual(new_instance.age, 30)
            self.assertEqual(new_instance.height, 5.9)

    def test_create_with_invalid_parameter(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create User name="Jane" invalid=param')
            instance_id = output.getvalue().strip()
            key = f"User.{instance_id}"
            self.assertIn(key, storage.all().keys())
            
            new_instance = storage.all()[key]
            self.assertEqual(new_instance.name, "Jane")
            with self.assertRaises(AttributeError):
                new_instance.invalid

    def test_create_with_escaped_quotes_and_underscores(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create User description="A_house_with_a_big_yard" quote="She_said_\\"Hello!\\""')
            instance_id = output.getvalue().strip()
            key = f"User.{instance_id}"
            self.assertIn(key, storage.all().keys())
            
            new_instance = storage.all()[key]
            self.assertEqual(new_instance.description, "A house with a big yard")
            self.assertEqual(new_instance.quote, 'She said "Hello!"')

    def test_create_without_parameters(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create User')
            instance_id = output.getvalue().strip()
            key = f"User.{instance_id}"
            self.assertIn(key, storage.all().keys())
            
            new_instance = storage.all()[key]
            self.assertTrue(hasattr(new_instance, "id"))

    def test_show(self):
        for item in self.__list:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd("create " + item)
                uid = output.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd("show " + item + " " + uid)
                result = output.getvalue().strip()
                key = item + "." + uid
                self.assertEqual(str(storage.all()[key]), result)
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(item + '.show("{}")'.format(uid))
                result1 = output.getvalue().strip()
                self.assertEqual(str(storage.all()[key]), result1)

    def test_destroy(self):
        for item in self.__list:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd("create " + item)
                uid = output.getvalue().strip()
                HBNBCommand().onecmd("destroy " + item + " " + uid)
                key = item + "." + uid
                self.assertNotIn(key, storage.all().keys())
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd("create " + item)
                uid = output.getvalue().strip()
                key = item + "." + uid
                HBNBCommand().onecmd(item + '.destroy("{}")'.format(uid))
                self.assertNotIn(key, storage.all().keys())

    def test_all(self):
        for item in self.__list:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd("create " + item)
                HBNBCommand().onecmd("all " + item)
                self.assertIn(item, output.getvalue().strip())
        for item in self.__list:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(item + ".all()")
                self.assertIn(item, output.getvalue().strip())

    def test_update(self):
        for item in self.__list:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd("create " + item)
                uid = output.getvalue().strip()
                HBNBCommand().onecmd("update " + item +
                                     " " + uid + " name Bob")
                self.assertTrue(len(output.getvalue().strip()) > 0)
                key = item + "." + uid
                self.assertEqual(storage.all()[key].name, "Bob")
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(
                    item + '.update({}, "name", "Monalisa")'.format(uid))
                key = item + "." + uid
                self.assertEqual(storage.all()[key].name, "Monalisa")

    def test_count(self):
        for item in self.__list:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(item + ".count()")
                count = output.getvalue().strip()
                objects = []
                for obj in storage.all().values():
                    if obj.__class__.__name__ == item:
                        objects.append(obj)

            self.assertEqual(int(count), len(objects))


if __name__ == "__main__":
    unittest.main()
