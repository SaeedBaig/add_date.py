# -*- coding: utf-8 -*-

"""Key-binding-activated command that automatically updates the
date-last-modified section in a file with each save.

Only thing the user has to change (if they so wish) are the variables
Header_Format and/or Date_Format.

Code adapted from hintermair's answer on: https://stackoverflow.com/questions/28032780/automatic-update-date-in-sublime-by-save

NOTE: Only change the variables Header_Format and/or Date_Format.
The rest of the code should remain untouched.
"""

import sublime
import sublime_plugin
import time


class AddDateCommand(sublime_plugin.TextCommand):
    """To update time/date last modified, command looks for the beginning
    of the date-line (e.g. "L" if it's "// Last Edited: 26 Jun 2017
    05:38PM") and the end of the date-line (e.g. "M" if it's "// Last Edited:
    26 Jun 2017 05:38PM") and replaces the whole string with an identical
    string (only change being the time/date).
    """

    def run(self, args):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        original_position = self.view.sel()[0]

        # Can change Header_Format to a different title if you so wish
        # (you don't have to add an extra space at the end of Header_Format;
        # the rest of the code already takes care of that for you).
        Header_Format = "Last Edited:"

        begin = content.find(Header_Format)

        # If there's no date-line in the file, nothing happens.
        if begin == -1:
            return
        # else:

        # If you want your date printed out in a different format
        # (e.g. YYYY/mm/dd instead of dd mm YYYY),
        # feel free to rearrange/play around with the parameters in strftime().
        Date_Format = time.strftime("%d %b %Y %I:%M%p")

        # The " " adds a space between Header_Format and Date_Format.
        date_line = Header_Format + " " + Date_Format
        end = begin + len(date_line)

        # Move the cursor to the region in the file where the header/date are.
        target_region = sublime.Region(begin, end)
        self.view.sel().clear()
        self.view.sel().add(target_region)

        # Update the date.
        self.view.run_command("insert_snippet", { "contents": date_line })

        # Move the cursor back to the original position the user was typing at
        # (so the screen doesn't move away too much from the user).
        self.view.sel().clear()
        self.view.sel().add(original_position)
        self.view.show(original_position)


class DateAndSaveCommand(sublime_plugin.WindowCommand):
    """Command does 2 things; save the file, and update the date-line."""

    def run(self):
        self.window.run_command("save")
        self.window.run_command("add_date")
        # We save again here, since the change-of-date itself needs to be saved
        self.window.run_command("save")
