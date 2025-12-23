# Folder Management Guide

## How to Delete Nested Folders

If you accidentally create nested folders with duplicate names (e.g., `folder/folder/`), here's how to fix it:

### Method 1: Using Git Commands
```bash
# Move files from nested folder to parent
git mv nested_folder/nested_folder/file.txt nested_folder/

# Remove the empty nested folder
git rm -r nested_folder/nested_folder/

# Commit the changes
git commit -m "Fix: Remove nested folder structure"
```

### Method 2: Using Standard Commands
```bash
# Move files from nested folder to parent
mv nested_folder/nested_folder/* nested_folder/

# Remove the empty nested folder
rmdir nested_folder/nested_folder/

# Stage and commit changes
git add .
git commit -m "Fix: Remove nested folder structure"
```

### Method 3: Using GUI Tools
- **VS Code**: Use the file explorer to drag and drop files, then delete empty folders
- **GitHub Desktop**: Move files in your file manager, then stage and commit in GitHub Desktop
- **File Manager**: Use your system's file manager to reorganize, then commit via command line

## Prevention Tips

1. **Check your current directory** before creating folders:
   ```bash
   pwd  # Print working directory
   ```

2. **Use tab completion** to avoid typos when creating directories:
   ```bash
   mkdir week1_<TAB>  # Auto-completes if folder exists
   ```

3. **List existing folders** before creating new ones:
   ```bash
   ls -la
   ```

4. **Use relative paths carefully**:
   ```bash
   # Bad: might create nested folders
   cd my_folder && mkdir my_folder
   
   # Good: check first, then create in correct location
   cd my_folder && ls  # Verify you're in the right place
   # If you need a new folder, create it with a different name
   mkdir new_folder_name
   ```

## Common Scenarios

### Scenario 1: Duplicate Folder Names
**Problem**: `week1_genai_foundations/week1_genai_foundations/`
**Solution**: Move contents up one level and remove nested folder

### Scenario 2: Deep Nesting
**Problem**: `folder1/folder2/folder3/folder4/file.txt`
**Solution**: Restructure to a flatter hierarchy if it makes sense

### Scenario 3: Mixed Content
**Problem**: Files in both parent and nested folders
**Solution**: Consolidate all files into the parent folder, ensuring no overwrites

## Quick Reference

| Command | Purpose |
|---------|---------|
| `mv source dest` | Move files or folders |
| `rmdir folder` | Remove empty directory |
| `rm -r folder` | Remove directory and contents (use with caution!) |
| `git mv old new` | Move and stage in one command |
| `git rm -r folder` | Remove folder from git tracking |
| `tree` or `ls -R` | View folder structure |

## Need Help?
If you're unsure about removing folders, you can always:
1. Create a backup branch: `git checkout -b backup-branch`
2. Make changes on the backup branch first
3. Review changes with `git status` and `git diff`
4. Only merge to main when you're confident
