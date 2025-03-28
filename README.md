## Introduction

- This is a miniature implementation of a dogbed database in Python.

**This simple DBDB implementation handles the following cases:**
1. Saves data to disk so it's not lost when the program ends.
2. It can handle crashes without corrupting the data.
3. It doesn't need to load all data into memory at once.

**ACID Properties Implemented**
- Atomicity: Changes are all or nothing
- Durability: Once saved, data remains stored