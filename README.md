# A keybinding-activated command to automatically update timestamps in Sublime Text on save.
**NOTE**: This command appears to work on Sublime Text 3, but I haven't tested it on Sublime Text 2 or earlier.

Do you like to have a "last edited" section in your source files?, to inform others (and your future self) of when you last edited the file? Something like this?

```C
/* 
 * Author: Me
 * Last Edited: 21 Nov 2017 12:32PM
 * Simple Hello World Program
 */

#include <stdio.h>
int main()
{
        puts("Hello World!");
        return 0;
}

```

but are tired of updating the date/time everytime you save the file? Wish there was a way to just make the datestamp update itself everytime you saved?

Well now there is! The code in the file ```add_date.py``` can do exactly just that.

## So how do I use this?
To use it, simply:
1. Save the file ```add_date.py``` in Sublime Text -> Packages -> User.
2. Go to Sublime Text -> Preferences -> Key Bindings, and add this into User:

```json
[
    {"keys": ["super+s"], "command": "date_and_save" }
]
```

That's it! Now any file you work on should have the datestamp (whose format you can change by changing the respective variable in ```add_date.py```; see ```add_date.py``` for further info) automatically updated whenever you press command+S (MIGHT be control+S on Windows).

So it would turn a file that may look something like this:
```C
/* 
 * Author: Me
 * Last Edited: 15 Oct 2017 11:15AM
 * Simple Hello World Program
 */

#include <stdio.h>
int main()
{
        puts("Hello World!");
        return 0;
}

```

into something like this upon hitting command+S:
```C
/* 
 * Author: Me
 * Last Edited: 21 Nov 2017 12:47PM
 * Simple Hello World Program
 */

#include <stdio.h>
int main()
{
        puts("Hello World!");
        return 0;
}

```

and not just for C files! Should work on files of any syntax. For example, it can turn a file like this:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Another simple "Hello World" program
# By Me
# Last Edited: 15 Oct 2017 11:15AM

print("Hello World")

```

...into this upon hitting command+S:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Another simple "Hello World" program
# By Me
# Last Edited: 21 Nov 2017 12:53PM

print("Hello World")

```

Again, if you want to change the format for the date/heading in your source files to something other than "Last Edited: dd mon year hh:mmPM", read the comments in ```add_date.py```, which will give you instructions on how to do that.

### ***But what if I want different formats for different syntaxes?***

Sometimes you may want to use a different format for your headings/dates depending on your file. For example, for your Python files you may want the date stored as a string in a magic variable for documentation purposes, like this:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A thoroughly-documented source file"""

__author__ = "Me <Me@icloud.com>"
__copyright__ = "Copyright © 2017 Me"
__date__ = "21 Nov 2017 01:11PM"

print("Hi")

```
but for your source files in other languages, you'd rather have a different heading or format, maybe like this:
```C
/*
 * Author: Me
 * Last Edited: 21 Nov 2017 01:14PM
 * Hi
 */

#include <stdio.h>

int main(void)
{
	puts("Hi");
	return EXIT_SUCCESS;
}

```

in THAT case... you'd need to edit the ```add_date.py``` file. But don't sweat. I've already done the hard work for you and figured out how you can do it. To achieve the kind of functionality I just described, the ```run``` function in ```add_date.py``` would be changed to look like this:
```python
def run(self, args):
    content = self.view.substr(sublime.Region(0, self.view.size()))
    original_position = self.view.sel()[0]
    syntax = self.view.settings().get("syntax")

    # Can change Header_Format to a different title if you so wish
    # (you don't have to add an extra space at the end of Header_Format;
    # the rest of the code already takes care of that for you).
    if "Python" in syntax:
        Header_Format = "__date__ ="
    else:
        Header_Format = "Last Edited:"

    begin = content.find(Header_Format)

    # If there's no date-line in the file, nothing happens.
    if begin == -1:
        return
    # else:

    # If you want your date printed out in a different format
    # (e.g. YYYY/mm/dd instead of dd mm YYYY),
    # feel free to rearrange/play around with the parameters in strftime().
    if Header_Format == "__date__ =":
        Date_Format = "\"" + time.strftime("%d %b %Y %I:%M%p") + "\""
    else:
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
```
Don't worry if that seems like a lot! It's only mildly different to the ```run``` function in the normal ```add_date.py``` file. It's not the most elegant solution, but hopefully you can see how selecting syntaxes work well enough here to be able to make your own syntax-specific formats by editing the ```run``` function appropriatey.

**KNOWN ISSUES**:
* You DO need some date string in the file to begin with for the formatting to stay the same. If u try hitting command + s on something like this:
```C
/* 
 * Author: Me
 * Last Edited:
 * Simple Hello World Program
 */

#include <stdio.h>
int main()
{
        puts("Hello World!");
        return 0;
}
```

you will get something mangled like this:
```C
/*
 * Author: Me
 * Last Edited: 21 Nov 2017 12:59PMld Program
 */

#include <stdio.h>
int main()
{
        puts("Hello World!");
        return 0;
}
```
But at least you'll only have to add the date format once (which I just use a Sublime Text snippet for anyways).
Hope this helps!

* The view will shift a bit everytime you save if your cursor isn't directly in the middle of the screen (i.e. Sublime Text will automatically scroll to make the line your cursor was on when you pressed command+S the centre of the view).
