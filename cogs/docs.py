import io, zlib, os, re
from datetime import datetime
from typing import Dict
import nextcord as discord
from nextcord.ext import commands
from .important import doc


class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode("utf-8")

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b""
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b"\n")
            while pos != -1:
                yield buf[:pos].decode("utf-8")
                buf = buf[pos + 1 :]
                pos = buf.find(b"\n")


class Docs(commands.Cog):
    """Search information in the nextcord documentation."""
    # full credit to https://github.com/Rapptz/RoboDanny
    def __init__(self, bot):
        self.bot = bot
    
    COG_EMOJI = "📚"

    def parse_object_inv(self, stream: SphinxObjectFileReader, url: str) -> Dict:
        result = {}
        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]  # not needed

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError("Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            key = (
                key.replace("nextcord.ext.commands.", "")
                .replace("nextcord.ext.menus.", "")
                .replace("nextcord.ext.ipc.", "")
                .replace("nextcord.", "")
            )

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_docs_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with self.bot.session.get(page + "/objects.inv") as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        "Cannot build docs lookup table, try again later."
                    )

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._docs_cache = cache
        c = discord.Client()
        await c.close()

    async def do_docs(self, ctx, key, obj):
        page_types = {
            "master": "https://nextcord.readthedocs.io/en/latest",
            "menus": "https://nextcord-ext-menus.readthedocs.io/en/latest",
            "ipc": "https://nextcord-ext-ipc.readthedocs.io/en/latest",
            "python": "https://docs.python.org/3",
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, "_docs_cache"):
            await ctx.trigger_typing()
            await self.build_docs_lookup_table(page_types)

        obj = re.sub(r"^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)
        obj = re.sub(r"^(?:nextcord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)

        if key.startswith("master"):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == "_":
                    continue
                if q == name:
                    obj = f"abc.Messageable.{name}"
                    break

        cache = list(self._docs_cache[key].items())

        def transform(tup):
            return tup[0]

        matches = doc.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send("Could not find anything. Sorry.")

        e.description = "\n".join(f"[`{key}`]({url})" for key, url in matches)
        ref = ctx.message.reference
        refer = None
        if ref and isinstance(ref.resolved, discord.Message):
            refer = ref.resolved.to_reference()
        await ctx.send(embed=e, reference=refer)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} MODULE] » Nextcord Docs enabled.\u001b[0m")

    @commands.group(name="docs", help="📚 - Searches in nextcord docs.", invoke_without_command=True)
    async def docs_group(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "master", obj)

    @docs_group.command(name="menus")
    async def docs_menu_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "menus", obj)

    @docs_group.command(name="ipc")
    async def docs_ipc_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "ipc", obj)

    @docs_group.command(name="python", aliases=["py"])
    async def docs_python_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_docs(ctx, "python", obj)

    @commands.command(
        help="🧹 - Delete cache of nextcord docs (owner only)", aliases=["purge-docs", "deldocs"]
    )
    @commands.is_owner()
    async def docscache(self, ctx: commands.Context):
        del self._docs_cache
        embed = discord.Embed(title="Purged docs cache.", color=discord.Color.blurple())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Docs(bot))