import webpack from 'webpack';
import path from 'path';


export default {
	debug: false,
	devtool: 'source-map',
	noInfo: false,
	entry: {
		app: ["./src/index.js"],
		vendor: [
			"jquery",
			"underscore",
			"stats.js",
			"three",
			"md5",
			"event-emitter-es6",
			"whatwg-fetch"]
	},
	target: 'web',
	output: {
		path: __dirname + '/static/js',
		filename: 'app.js',
	},
	plugins: [
		new webpack.DefinePlugin({PRODUCTION: JSON.stringify(false),}),
		new webpack.optimize.CommonsChunkPlugin("vendor", "vendor.js"),
		/*new webpack.optimize.OccurenceOrderPlugin(),
		new webpack.optimize.DedupePlugin(),
		new webpack.optimize.UglifyJsPlugin({
			minimize: true,
			mangle: true
		})*/
	],

	module: {
		loaders: [
			{test: /\.js$/, include: path.join(__dirname, 'src'), loaders: ['babel']}
		]
	},
};
