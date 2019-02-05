const fs = require("fs")
const Path = require("path")

const Bundler = require("parcel-bundler")
const yaml = require("js-yaml")
const cliOpts = require("yargs").parse()


const configFile = cliOpts.config ? `${ process.cwd() }/${ cliOpts.config }` : null
const environment = process.env.NODE_ENV || "dev"

// read in local config file
const config = yaml.load(fs.readFileSync(configFile))

class Bundle {
    constructor() {
        this.importContext = `${ process.cwd() }/${ config.src }`
        this.exportContext = this.setExportContext(config.build)

        this.sources = config.entries
        this.buildDir = config.output
        this.entries = this.setEntries(config.entries)
        this.aliases = config.aliases || false
        this.options = this.setOptions()
        this.bundler = {}
    }

    setExportContext(context = "../") {
        // @info  create directory if it doesn't exist
        if (!fs.existsSync(context)) fs.mkdirSync(context)
        process.chdir(context)
        return process.cwd()
    }

    // Entrypoint file location(s)
    setEntries(entries) {
        // @info  map your entry files to give them their own names (in case different!)
        this.sources = new Map(
            Object.entries(entries)
                .map( ([key, value]) => [value, key] )
        )

        // @enhancement right now we manually add the blob stars, but maybe later we do it auto.
        return entries
            ? Object.values(entries)
                .map( entry => Path.join(this.importContext, `./${entry}`) )
            : Path.join(this.importContext, `./**/*.*`) // this is a backup plan but recommend against.
    }

    // @desc    set up Bundler options
    setOptions() {
        return {
            // @desc    make false for build inspection and testing
            cache: false,

            // @desc    we want to control the file names ourselves
            contentHash: false,

            // @desc    The out directory to put the build files in
            // @        parcel defaults to dist, we default to 'static'
            outDir: Path.join(this.exportContext, this.buildDir || "../static"),

            publicUrl: `/${this.buildDir}`,

            // @dssc    3 = log everything, 2 = log warnings & errors, 1 = log errors
            logLevel: 3,

            // @desc    we only want to watch files when developing
            watch: environment !== "production" ? true : false,

            // @desc    we will minify outside of Parcel in order to get more control
            minify: false,

            // @desc    not using sourceMaps for now
            sourceMaps: false,

            hmr: true,
            hmrPort: 0,

            // @desc    Prints a detailed report of the bundles, assets, filesizes and times
            // @        defaults to false, reports are only printed if watch is disabled
            detailedReport: true,

            // @desc    parcel can autoinstall NPM assets,
            // @        we want to make sure we have te most control
            autoinstall: false
        }
    }

    // @desc    Initialises a bundler using the entrypoint location and options provided
    async run() {
        this.bundler = new Bundler(this.entries, this.options)

        // -  the bundler ignores / overwrites custom/certain options; override here
        this.bundler.options.rootDir = Path.join(this.importContext)

        // -  here we bring in the aliasing from the yaml config, so we don't need separate files
        this.bundler.options.aliases = this.aliases

        // for pathing, should we need it
        this.bundler.options.buildConfig = this.config

        // HACK: parcel aggressively bundles hrefs/sources/etc that we want to handle outside the bundler, so we hack it here.
        this.bundler.addAssetType("html", require.resolve("./parcel/HTMLAsset.js"))

        // console.log(this.bundler.options.aliases)
        await this.bundler.bundle()
    }

    // @info    outputs to the console a representation of the current class to see its internals
    getSelf() {
        console.log(this)
    }
}

const butter = new Bundle()
butter.run()
