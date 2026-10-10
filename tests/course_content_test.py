"""Check file edits reach the actual static reader and downloadable Markdown."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_module1
from course_content import CONTENT, load_course, module_source


class CourseContentTests(unittest.TestCase):
    def test_lesson_edit_reaches_reader_and_download(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / 'content/course'
            shutil.copytree(CONTENT, folder)
            (root / 'docs/chapters').mkdir(parents=True)
            shutil.copy(ROOT / 'docs/chapters/01.html', root / 'docs/chapters/01.html')
            lesson = folder / '02-week.md'
            marker = 'Перевірка зміни окремого уроку <script>test</script>'
            lesson.write_text(lesson.read_text().replace('## Урок 8.', marker + '\n\n## Урок 8.', 1))
            with patch.object(build_module1, 'ROOT', root):
                build_module1.build(1, folder)
            html = (root / 'docs/chapters/01.html').read_text()
            section = html.split('id="page-8"')[1].split('</section>')[0]
            self.assertIn('Перевірка зміни окремого уроку &lt;script&gt;test&lt;/script&gt;', section)
            self.assertIn(marker, (root / 'docs/module1.md').read_text())
            self.assertEqual(html.count('data-extended="true"'), 1)

    def test_incomplete_or_misnumbered_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(CONTENT, root, dirs_exist_ok=True)
            lesson = root / '02-week.md'
            lesson.write_text(lesson.read_text().replace('## Урок 5.', '## Урок 6.', 1))
            with self.assertRaisesRegex(ValueError, 'expected lessons 5–8'):
                load_course(root)
            lesson.unlink()
            with self.assertRaisesRegex(ValueError, 'expected 18 Markdown files'):
                module_source(1, root)


if __name__ == '__main__':
    unittest.main()
