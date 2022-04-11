import sys
from contextlib import contextmanager
from functools import wraps
from typing import Union, List, Optional

import discord
from discord.ext.bridge import BridgeContext
from discord.ext.commands import Context


# Custom error messages

@contextmanager
def disable_exception_traceback():
    """
    All traceback information is suppressed and only the exception type and value are printed
    """
    default_value = getattr(sys, "tracebacklimit", 1000)  # `1000` is a Python's default value
    sys.tracebacklimit = 0
    yield
    sys.tracebacklimit = default_value  # revert changes


class PermissionAbuseWarning(Exception):
    """
    A warning message.
    """

    def __init__(self, user_name: str, message: Optional[str] = None):
        super().__init__(message or f"{user_name} attempted to run a command that they do not have permission to run.")


# Custom functions

async def send_error(ctx: Union[BridgeContext, Context], error_message: Optional[str] = None):
    await ctx.respond(error_message or "Something went wrong!")


def get_roles(guild: discord.Guild, role_names: List[str]) -> List[discord.Role]:
    filtered_roles = []
    for role in guild.roles:
        if role.name in role_names:
            filtered_roles.append(role)
    return filtered_roles


def get_users(guild: discord.Guild, user_ids: List[int]) -> List[discord.Member]:
    members = []
    for member in guild.members:
        if member.id in user_ids:
            members.append(member)
    return members


def get_users_with_roles(guild: discord.Guild, role_names: List[str]) -> List[discord.Member]:
    members = []
    roles = get_roles(guild, role_names)
    for member in guild.members:
        if any(x in member.roles for x in roles):
            members.append(member)
    return members


def get_users_without_roles(guild: discord.Guild, role_names: List[str]) -> List[discord.Member]:
    members = []
    roles = get_roles(guild, role_names)
    for member in guild.members:
        if not any(x in member.roles for x in roles):
            members.append(member)
    return members


def user_has_role(user: discord.Member, role_name: str) -> bool:
    role = discord.utils.get(user.guild.roles, name=role_name)
    return role in user.roles


def user_does_not_have_role(user: discord.Member, role_name: str) -> bool:
    role = discord.utils.get(user.guild.roles, name=role_name)
    return role not in user.roles


async def user_is_admin(cog: 'BaseCog', ctx: Union[BridgeContext, Context]) -> bool:
    # TODO: improve speed on this later
    # check IDs first, most likely less of them, but more strict
    admin_ids = cog.get_admin_users(guild=ctx.guild)
    if admin_ids and any(x in ctx.author.id for x in admin_ids):
        return True
    # check admin roles next
    admin_roles = cog.get_admin_roles(guild=ctx.guild)
    if admin_roles and any(x in ctx.author.roles for x in admin_roles):
        return True
    return False


# Custom decorators

def is_admin(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        cog = args[0]
        ctx = args[1]
        if await user_is_admin(cog=cog, ctx=ctx):
            return await func(*args, **kwargs)
        await send_error(ctx=ctx, error_message="You are not an admin!")
        with disable_exception_traceback():
            raise PermissionAbuseWarning(user_name=ctx.author.name)

    return inner
