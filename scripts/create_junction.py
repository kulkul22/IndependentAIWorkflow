import sys
import os

def create_junction(link_path, target_path):
    target_path = os.path.abspath(target_path)
    link_path = os.path.abspath(link_path)
    
    if not os.path.exists(target_path):
        print(f"Error: Target path does not exist: {target_path}")
        sys.exit(1)
        
    try:
        import _winapi
        # _winapi.CreateJunction(src_path, dst_path)
        _winapi.CreateJunction(target_path, link_path)
        print(f"Junction created: {link_path} -> {target_path}")
    except ImportError:
        # Fallback for non-Windows
        os.symlink(target_path, link_path, target_is_directory=True)
        print(f"Symlink created: {link_path} -> {target_path}")
    except Exception as e:
        print(f"Error creating junction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_junction.py <link_path> <target_path>")
        sys.exit(1)
    create_junction(sys.argv[1], sys.argv[2])
