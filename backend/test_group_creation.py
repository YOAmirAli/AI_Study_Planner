"""
Test script to verify group creation and database storage
This script tests the complete group creation flow
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from app import create_app
from app.config.database import db
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User
from app.services.group_service import GroupService

def test_group_creation():
    """Test group creation and database storage"""
    
    print("=" * 80)
    print("Testing Group Creation and Database Storage")
    print("=" * 80)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Step 1: Check if we have any users
            print("\n1. Checking for existing users...")
            users = User.query.all()
            if not users:
                print("   ✗ No users found in database!")
                print("   Please register a user first through the API")
                return False
            
            test_user = users[0]
            print(f"   ✓ Found user: {test_user.name} (ID: {test_user.user_id})")
            
            # Step 2: Test join code generation
            print("\n2. Testing join code generation...")
            join_code = GroupService._generate_join_code()
            print(f"   ✓ Generated join code: {join_code}")
            print(f"   ✓ Code length: {len(join_code)} characters")
            print(f"   ✓ Code format: Mixed uppercase letters and digits")
            
            # Step 3: Create a test group
            print("\n3. Creating test group...")
            group_data, error = GroupService.create_group(
                admin_user_id=test_user.user_id,
                group_name="Test Study Group",
                description="This is a test group for verification",
                is_private=False,
                max_members=20
            )
            
            if error:
                print(f"   ✗ Error creating group: {error}")
                return False
            
            print(f"   ✓ Group created successfully!")
            print(f"   ✓ Group ID: {group_data['group_id']}")
            print(f"   ✓ Group Name: {group_data['group_name']}")
            print(f"   ✓ Join Code: {group_data['join_code']}")
            print(f"   ✓ Admin User ID: {group_data['admin_user_id']}")
            print(f"   ✓ Member Count: {group_data['member_count']}")
            
            # Step 4: Verify group exists in database
            print("\n4. Verifying group in database...")
            db_group = Group.query.get(group_data['group_id'])
            if not db_group:
                print("   ✗ Group not found in database!")
                return False
            
            print(f"   ✓ Group found in database")
            print(f"   ✓ Database Group ID: {db_group.group_id}")
            print(f"   ✓ Database Group Name: {db_group.group_name}")
            print(f"   ✓ Database Join Code: {db_group.join_code}")
            
            # Step 5: Verify group member exists
            print("\n5. Verifying group membership...")
            membership = GroupMember.query.filter_by(
                group_id=db_group.group_id,
                user_id=test_user.user_id
            ).first()
            
            if not membership:
                print("   ✗ Group membership not found!")
                return False
            
            print(f"   ✓ Membership found")
            print(f"   ✓ User ID: {membership.user_id}")
            print(f"   ✓ Role: {membership.role}")
            print(f"   ✓ Joined At: {membership.joined_at}")
            
            # Step 6: Test join by code
            print("\n6. Testing join by code functionality...")
            if len(users) > 1:
                second_user = users[1]
                join_result, join_error = GroupService.join_group_by_code(
                    join_code=db_group.join_code,
                    user_id=second_user.user_id
                )
                
                if join_error:
                    print(f"   ✗ Error joining group: {join_error}")
                else:
                    print(f"   ✓ User {second_user.name} joined successfully!")
                    print(f"   ✓ New member count: {join_result['member_count']}")
            else:
                print("   ⚠ Only one user available, skipping join test")
            
            # Step 7: List all groups
            print("\n7. Listing all groups in database...")
            all_groups = Group.query.all()
            print(f"   ✓ Total groups: {len(all_groups)}")
            for group in all_groups:
                print(f"   - {group.group_name} (Code: {group.join_code}, Members: {len(group.members)})")
            
            # Step 8: Clean up test group (optional)
            print("\n8. Cleaning up test group...")
            response = input("   Do you want to delete the test group? (y/n): ")
            if response.lower() == 'y':
                db.session.delete(db_group)
                db.session.commit()
                print("   ✓ Test group deleted")
            else:
                print("   ⚠ Test group kept in database")
            
            print("\n" + "=" * 80)
            print("✓ ALL TESTS PASSED!")
            print("=" * 80)
            return True
            
        except Exception as e:
            print(f"\n✗ Error during testing: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_group_creation()
    sys.exit(0 if success else 1)
