from django.db import migrations


PROJECT_MANAGER = 'Проектный менеджер'
TEAM_LEAD = 'Тим лид'
DEVELOPER = 'разраб'


def get_permission(Permission, ContentType, model_name, codename, name):
    content_type, _ = ContentType.objects.get_or_create(app_label='taskman', model=model_name)
    permission, _ = Permission.objects.get_or_create(
        content_type=content_type,
        codename=codename,
        defaults={'name': name},
    )
    return permission


def add_permissions(group, permissions):
    group.permissions.add(*permissions)


def create_role_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    project_manager, _ = Group.objects.get_or_create(name=PROJECT_MANAGER)
    team_lead, _ = Group.objects.get_or_create(name=TEAM_LEAD)
    developer, _ = Group.objects.get_or_create(name=DEVELOPER)

    permissions = {
        'add_project': get_permission(Permission, ContentType, 'project', 'add_project', 'Can add project'),
        'change_project': get_permission(Permission, ContentType, 'project', 'change_project', 'Can change project'),
        'delete_project': get_permission(Permission, ContentType, 'project', 'delete_project', 'Can delete project'),
        'view_project': get_permission(Permission, ContentType, 'project', 'view_project', 'Can view project'),
        'manage_project_users': get_permission(Permission, ContentType, 'project', 'manage_project_users', 'Can manage project users'),
        'add_task': get_permission(Permission, ContentType, 'task', 'add_task', 'Can add task'),
        'change_task': get_permission(Permission, ContentType, 'task', 'change_task', 'Can change task'),
        'delete_task': get_permission(Permission, ContentType, 'task', 'delete_task', 'Can delete task'),
        'view_task': get_permission(Permission, ContentType, 'task', 'view_task', 'Can view task'),
    }

    add_permissions(project_manager, [
        permissions['add_project'],
        permissions['change_project'],
        permissions['delete_project'],
        permissions['view_project'],
        permissions['manage_project_users'],
        permissions['add_task'],
        permissions['change_task'],
        permissions['delete_task'],
        permissions['view_task'],
    ])
    add_permissions(team_lead, [
        permissions['view_project'],
        permissions['manage_project_users'],
        permissions['add_task'],
        permissions['change_task'],
        permissions['delete_task'],
        permissions['view_task'],
    ])
    add_permissions(developer, [
        permissions['view_project'],
        permissions['add_task'],
        permissions['change_task'],
        permissions['view_task'],
    ])


def remove_role_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=[PROJECT_MANAGER, TEAM_LEAD, DEVELOPER]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taskman', '0007_alter_project_options'),
    ]

    operations = [
        migrations.RunPython(create_role_groups, remove_role_groups),
    ]
