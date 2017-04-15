// Common aliases
var $Reader = protobuf.Reader, $Writer = protobuf.Writer, $util = protobuf.util;

Spectrum = (function() {

    /**
     * Properties of a Spectrum.
     * @typedef Spectrum$Properties
     * @type {Object}
     * @property {Array.<number>} [R] Spectrum R.
     * @property {Array.<number>} [G] Spectrum G.
     * @property {Array.<number>} [B] Spectrum B.
     * @property {Array.<number>} [A] Spectrum A.
     * @property {Array.<number>} [H] Spectrum H.
     * @property {Array.<number>} [S] Spectrum S.
     * @property {Array.<number>} [L] Spectrum L.
     */

    /**
     * Constructs a new Spectrum.
     * @exports Spectrum
     * @constructor
     * @param {Spectrum$Properties=} [properties] Properties to set
     */
    function Spectrum(properties) {
        this.R = [];
        this.G = [];
        this.B = [];
        this.A = [];
        this.H = [];
        this.S = [];
        this.L = [];
        if (properties)
            for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                if (properties[keys[i]] != null)
                    this[keys[i]] = properties[keys[i]];
    }

    /**
     * Spectrum R.
     * @type {Array.<number>}
     */
    Spectrum.prototype.R = $util.emptyArray;

    /**
     * Spectrum G.
     * @type {Array.<number>}
     */
    Spectrum.prototype.G = $util.emptyArray;

    /**
     * Spectrum B.
     * @type {Array.<number>}
     */
    Spectrum.prototype.B = $util.emptyArray;

    /**
     * Spectrum A.
     * @type {Array.<number>}
     */
    Spectrum.prototype.A = $util.emptyArray;

    /**
     * Spectrum H.
     * @type {Array.<number>}
     */
    Spectrum.prototype.H = $util.emptyArray;

    /**
     * Spectrum S.
     * @type {Array.<number>}
     */
    Spectrum.prototype.S = $util.emptyArray;

    /**
     * Spectrum L.
     * @type {Array.<number>}
     */
    Spectrum.prototype.L = $util.emptyArray;

    /**
     * Creates a new Spectrum instance using the specified properties.
     * @param {Spectrum$Properties=} [properties] Properties to set
     * @returns {Spectrum} Spectrum instance
     */
    Spectrum.create = function create(properties) {
        return new Spectrum(properties);
    };

    /**
     * Encodes the specified Spectrum message. Does not implicitly {@link Spectrum.verify|verify} messages.
     * @param {Spectrum$Properties} message Spectrum message or plain object to encode
     * @param {protobuf.Writer} [writer] Writer to encode to
     * @returns {protobuf.Writer} Writer
     */
    Spectrum.encode = function encode(message, writer) {
        if (!writer)
            writer = $Writer.create();
        if (message.R != null && message.R.length) {
            writer.uint32(/* id 1, wireType 2 =*/10).fork();
            for (var i = 0; i < message.R.length; ++i)
                writer.int32(message.R[i]);
            writer.ldelim();
        }
        if (message.G != null && message.G.length) {
            writer.uint32(/* id 2, wireType 2 =*/18).fork();
            for (var i = 0; i < message.G.length; ++i)
                writer.int32(message.G[i]);
            writer.ldelim();
        }
        if (message.B != null && message.B.length) {
            writer.uint32(/* id 3, wireType 2 =*/26).fork();
            for (var i = 0; i < message.B.length; ++i)
                writer.int32(message.B[i]);
            writer.ldelim();
        }
        if (message.A != null && message.A.length) {
            writer.uint32(/* id 4, wireType 2 =*/34).fork();
            for (var i = 0; i < message.A.length; ++i)
                writer.int32(message.A[i]);
            writer.ldelim();
        }
        if (message.H != null && message.H.length) {
            writer.uint32(/* id 5, wireType 2 =*/42).fork();
            for (var i = 0; i < message.H.length; ++i)
                writer.int32(message.H[i]);
            writer.ldelim();
        }
        if (message.S != null && message.S.length) {
            writer.uint32(/* id 6, wireType 2 =*/50).fork();
            for (var i = 0; i < message.S.length; ++i)
                writer.int32(message.S[i]);
            writer.ldelim();
        }
        if (message.L != null && message.L.length) {
            writer.uint32(/* id 7, wireType 2 =*/58).fork();
            for (var i = 0; i < message.L.length; ++i)
                writer.int32(message.L[i]);
            writer.ldelim();
        }
        return writer;
    };

    /**
     * Encodes the specified Spectrum message, length delimited. Does not implicitly {@link Spectrum.verify|verify} messages.
     * @param {Spectrum$Properties} message Spectrum message or plain object to encode
     * @param {protobuf.Writer} [writer] Writer to encode to
     * @returns {protobuf.Writer} Writer
     */
    Spectrum.encodeDelimited = function encodeDelimited(message, writer) {
        return this.encode(message, writer).ldelim();
    };

    /**
     * Decodes a Spectrum message from the specified reader or buffer.
     * @param {protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
     * @param {number} [length] Message length if known beforehand
     * @returns {Spectrum} Spectrum
     * @throws {Error} If the payload is not a reader or valid buffer
     * @throws {protobuf.util.ProtocolError} If required fields are missing
     */
    Spectrum.decode = function decode(reader, length) {
        if (!(reader instanceof $Reader))
            reader = $Reader.create(reader);
        var end = length === undefined ? reader.len : reader.pos + length, message = new Spectrum();
        while (reader.pos < end) {
            var tag = reader.uint32();
            switch (tag >>> 3) {
            case 1:
                if (!(message.R && message.R.length))
                    message.R = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.R.push(reader.int32());
                } else
                    message.R.push(reader.int32());
                break;
            case 2:
                if (!(message.G && message.G.length))
                    message.G = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.G.push(reader.int32());
                } else
                    message.G.push(reader.int32());
                break;
            case 3:
                if (!(message.B && message.B.length))
                    message.B = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.B.push(reader.int32());
                } else
                    message.B.push(reader.int32());
                break;
            case 4:
                if (!(message.A && message.A.length))
                    message.A = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.A.push(reader.int32());
                } else
                    message.A.push(reader.int32());
                break;
            case 5:
                if (!(message.H && message.H.length))
                    message.H = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.H.push(reader.int32());
                } else
                    message.H.push(reader.int32());
                break;
            case 6:
                if (!(message.S && message.S.length))
                    message.S = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.S.push(reader.int32());
                } else
                    message.S.push(reader.int32());
                break;
            case 7:
                if (!(message.L && message.L.length))
                    message.L = [];
                if ((tag & 7) === 2) {
                    var end2 = reader.uint32() + reader.pos;
                    while (reader.pos < end2)
                        message.L.push(reader.int32());
                } else
                    message.L.push(reader.int32());
                break;
            default:
                reader.skipType(tag & 7);
                break;
            }
        }
        return message;
    };

    /**
     * Decodes a Spectrum message from the specified reader or buffer, length delimited.
     * @param {protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
     * @returns {Spectrum} Spectrum
     * @throws {Error} If the payload is not a reader or valid buffer
     * @throws {protobuf.util.ProtocolError} If required fields are missing
     */
    Spectrum.decodeDelimited = function decodeDelimited(reader) {
        if (!(reader instanceof $Reader))
            reader = $Reader(reader);
        return this.decode(reader, reader.uint32());
    };

    /**
     * Verifies a Spectrum message.
     * @param {Object.<string,*>} message Plain object to verify
     * @returns {?string} `null` if valid, otherwise the reason why it is not
     */
    Spectrum.verify = function verify(message) {
        if (typeof message !== "object" || message === null)
            return "object expected";
        if (message.R != null && message.hasOwnProperty("R")) {
            if (!Array.isArray(message.R))
                return "R: array expected";
            for (var i = 0; i < message.R.length; ++i)
                if (!$util.isInteger(message.R[i]))
                    return "R: integer[] expected";
        }
        if (message.G != null && message.hasOwnProperty("G")) {
            if (!Array.isArray(message.G))
                return "G: array expected";
            for (var i = 0; i < message.G.length; ++i)
                if (!$util.isInteger(message.G[i]))
                    return "G: integer[] expected";
        }
        if (message.B != null && message.hasOwnProperty("B")) {
            if (!Array.isArray(message.B))
                return "B: array expected";
            for (var i = 0; i < message.B.length; ++i)
                if (!$util.isInteger(message.B[i]))
                    return "B: integer[] expected";
        }
        if (message.A != null && message.hasOwnProperty("A")) {
            if (!Array.isArray(message.A))
                return "A: array expected";
            for (var i = 0; i < message.A.length; ++i)
                if (!$util.isInteger(message.A[i]))
                    return "A: integer[] expected";
        }
        if (message.H != null && message.hasOwnProperty("H")) {
            if (!Array.isArray(message.H))
                return "H: array expected";
            for (var i = 0; i < message.H.length; ++i)
                if (!$util.isInteger(message.H[i]))
                    return "H: integer[] expected";
        }
        if (message.S != null && message.hasOwnProperty("S")) {
            if (!Array.isArray(message.S))
                return "S: array expected";
            for (var i = 0; i < message.S.length; ++i)
                if (!$util.isInteger(message.S[i]))
                    return "S: integer[] expected";
        }
        if (message.L != null && message.hasOwnProperty("L")) {
            if (!Array.isArray(message.L))
                return "L: array expected";
            for (var i = 0; i < message.L.length; ++i)
                if (!$util.isInteger(message.L[i]))
                    return "L: integer[] expected";
        }
        return null;
    };

    /**
     * Creates a Spectrum message from a plain object. Also converts values to their respective internal types.
     * @param {Object.<string,*>} object Plain object
     * @returns {Spectrum} Spectrum
     */
    Spectrum.fromObject = function fromObject(object) {
        if (object instanceof Spectrum)
            return object;
        var message = new Spectrum();
        if (object.R) {
            if (!Array.isArray(object.R))
                throw TypeError(".Spectrum.R: array expected");
            message.R = [];
            for (var i = 0; i < object.R.length; ++i)
                message.R[i] = object.R[i] | 0;
        }
        if (object.G) {
            if (!Array.isArray(object.G))
                throw TypeError(".Spectrum.G: array expected");
            message.G = [];
            for (var i = 0; i < object.G.length; ++i)
                message.G[i] = object.G[i] | 0;
        }
        if (object.B) {
            if (!Array.isArray(object.B))
                throw TypeError(".Spectrum.B: array expected");
            message.B = [];
            for (var i = 0; i < object.B.length; ++i)
                message.B[i] = object.B[i] | 0;
        }
        if (object.A) {
            if (!Array.isArray(object.A))
                throw TypeError(".Spectrum.A: array expected");
            message.A = [];
            for (var i = 0; i < object.A.length; ++i)
                message.A[i] = object.A[i] | 0;
        }
        if (object.H) {
            if (!Array.isArray(object.H))
                throw TypeError(".Spectrum.H: array expected");
            message.H = [];
            for (var i = 0; i < object.H.length; ++i)
                message.H[i] = object.H[i] | 0;
        }
        if (object.S) {
            if (!Array.isArray(object.S))
                throw TypeError(".Spectrum.S: array expected");
            message.S = [];
            for (var i = 0; i < object.S.length; ++i)
                message.S[i] = object.S[i] | 0;
        }
        if (object.L) {
            if (!Array.isArray(object.L))
                throw TypeError(".Spectrum.L: array expected");
            message.L = [];
            for (var i = 0; i < object.L.length; ++i)
                message.L[i] = object.L[i] | 0;
        }
        return message;
    };

    /**
     * Creates a Spectrum message from a plain object. Also converts values to their respective internal types.
     * This is an alias of {@link Spectrum.fromObject}.
     * @function
     * @param {Object.<string,*>} object Plain object
     * @returns {Spectrum} Spectrum
     */
    Spectrum.from = Spectrum.fromObject;

    /**
     * Creates a plain object from a Spectrum message. Also converts values to other types if specified.
     * @param {Spectrum} message Spectrum
     * @param {protobuf.ConversionOptions} [options] Conversion options
     * @returns {Object.<string,*>} Plain object
     */
    Spectrum.toObject = function toObject(message, options) {
        if (!options)
            options = {};
        var object = {};
        if (options.arrays || options.defaults) {
            object.R = [];
            object.G = [];
            object.B = [];
            object.A = [];
            object.H = [];
            object.S = [];
            object.L = [];
        }
        if (message.R && message.R.length) {
            object.R = [];
            for (var j = 0; j < message.R.length; ++j)
                object.R[j] = message.R[j];
        }
        if (message.G && message.G.length) {
            object.G = [];
            for (var j = 0; j < message.G.length; ++j)
                object.G[j] = message.G[j];
        }
        if (message.B && message.B.length) {
            object.B = [];
            for (var j = 0; j < message.B.length; ++j)
                object.B[j] = message.B[j];
        }
        if (message.A && message.A.length) {
            object.A = [];
            for (var j = 0; j < message.A.length; ++j)
                object.A[j] = message.A[j];
        }
        if (message.H && message.H.length) {
            object.H = [];
            for (var j = 0; j < message.H.length; ++j)
                object.H[j] = message.H[j];
        }
        if (message.S && message.S.length) {
            object.S = [];
            for (var j = 0; j < message.S.length; ++j)
                object.S[j] = message.S[j];
        }
        if (message.L && message.L.length) {
            object.L = [];
            for (var j = 0; j < message.L.length; ++j)
                object.L[j] = message.L[j];
        }
        return object;
    };

    /**
     * Creates a plain object from this Spectrum message. Also converts values to other types if specified.
     * @param {protobuf.ConversionOptions} [options] Conversion options
     * @returns {Object.<string,*>} Plain object
     */
    Spectrum.prototype.toObject = function toObject(options) {
        return this.constructor.toObject(this, options);
    };

    /**
     * Converts this Spectrum to JSON.
     * @returns {Object.<string,*>} JSON object
     */
    Spectrum.prototype.toJSON = function toJSON() {
        return this.constructor.toObject(this, protobuf.util.toJSONOptions);
    };

    return Spectrum;
})();

Transmission = (function() {

    /**
     * Properties of a Transmission.
     * @typedef Transmission$Properties
     * @type {Object}
     * @property {number|Long} [Timestamp] Transmission Timestamp.
     * @property {string} [Name] Transmission Name.
     * @property {string} [Entropy] Transmission Entropy.
     * @property {Spectrum$Properties} [Spectrum] Transmission Spectrum.
     */

    /**
     * Constructs a new Transmission.
     * @exports Transmission
     * @constructor
     * @param {Transmission$Properties=} [properties] Properties to set
     */
    function Transmission(properties) {
        if (properties)
            for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                if (properties[keys[i]] != null)
                    this[keys[i]] = properties[keys[i]];
    }

    /**
     * Transmission Timestamp.
     * @type {number|Long}
     */
    Transmission.prototype.Timestamp = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

    /**
     * Transmission Name.
     * @type {string}
     */
    Transmission.prototype.Name = "";

    /**
     * Transmission Entropy.
     * @type {string}
     */
    Transmission.prototype.Entropy = "";

    /**
     * Transmission Spectrum.
     * @type {(Spectrum$Properties|null)}
     */
    Transmission.prototype.Spectrum = null;

    /**
     * Creates a new Transmission instance using the specified properties.
     * @param {Transmission$Properties=} [properties] Properties to set
     * @returns {Transmission} Transmission instance
     */
    Transmission.create = function create(properties) {
        return new Transmission(properties);
    };

    /**
     * Encodes the specified Transmission message. Does not implicitly {@link Transmission.verify|verify} messages.
     * @param {Transmission$Properties} message Transmission message or plain object to encode
     * @param {protobuf.Writer} [writer] Writer to encode to
     * @returns {protobuf.Writer} Writer
     */
    Transmission.encode = function encode(message, writer) {
        if (!writer)
            writer = $Writer.create();
        if (message.Timestamp != null && message.hasOwnProperty("Timestamp"))
            writer.uint32(/* id 1, wireType 0 =*/8).int64(message.Timestamp);
        if (message.Name != null && message.hasOwnProperty("Name"))
            writer.uint32(/* id 2, wireType 2 =*/18).string(message.Name);
        if (message.Entropy != null && message.hasOwnProperty("Entropy"))
            writer.uint32(/* id 3, wireType 2 =*/26).string(message.Entropy);
        if (message.Spectrum != null && message.hasOwnProperty("Spectrum"))
            Spectrum.encode(message.Spectrum, writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
        return writer;
    };

    /**
     * Encodes the specified Transmission message, length delimited. Does not implicitly {@link Transmission.verify|verify} messages.
     * @param {Transmission$Properties} message Transmission message or plain object to encode
     * @param {protobuf.Writer} [writer] Writer to encode to
     * @returns {protobuf.Writer} Writer
     */
    Transmission.encodeDelimited = function encodeDelimited(message, writer) {
        return this.encode(message, writer).ldelim();
    };

    /**
     * Decodes a Transmission message from the specified reader or buffer.
     * @param {protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
     * @param {number} [length] Message length if known beforehand
     * @returns {Transmission} Transmission
     * @throws {Error} If the payload is not a reader or valid buffer
     * @throws {protobuf.util.ProtocolError} If required fields are missing
     */
    Transmission.decode = function decode(reader, length) {
        if (!(reader instanceof $Reader))
            reader = $Reader.create(reader);
        var end = length === undefined ? reader.len : reader.pos + length, message = new Transmission();
        while (reader.pos < end) {
            var tag = reader.uint32();
            switch (tag >>> 3) {
            case 1:
                message.Timestamp = reader.int64();
                break;
            case 2:
                message.Name = reader.string();
                break;
            case 3:
                message.Entropy = reader.string();
                break;
            case 4:
                message.Spectrum = Spectrum.decode(reader, reader.uint32());
                break;
            default:
                reader.skipType(tag & 7);
                break;
            }
        }
        return message;
    };

    /**
     * Decodes a Transmission message from the specified reader or buffer, length delimited.
     * @param {protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
     * @returns {Transmission} Transmission
     * @throws {Error} If the payload is not a reader or valid buffer
     * @throws {protobuf.util.ProtocolError} If required fields are missing
     */
    Transmission.decodeDelimited = function decodeDelimited(reader) {
        if (!(reader instanceof $Reader))
            reader = $Reader(reader);
        return this.decode(reader, reader.uint32());
    };

    /**
     * Verifies a Transmission message.
     * @param {Object.<string,*>} message Plain object to verify
     * @returns {?string} `null` if valid, otherwise the reason why it is not
     */
    Transmission.verify = function verify(message) {
        if (typeof message !== "object" || message === null)
            return "object expected";
        if (message.Timestamp != null && message.hasOwnProperty("Timestamp"))
            if (!$util.isInteger(message.Timestamp) && !(message.Timestamp && $util.isInteger(message.Timestamp.low) && $util.isInteger(message.Timestamp.high)))
                return "Timestamp: integer|Long expected";
        if (message.Name != null && message.hasOwnProperty("Name"))
            if (!$util.isString(message.Name))
                return "Name: string expected";
        if (message.Entropy != null && message.hasOwnProperty("Entropy"))
            if (!$util.isString(message.Entropy))
                return "Entropy: string expected";
        if (message.Spectrum != null && message.hasOwnProperty("Spectrum")) {
            var error = Spectrum.verify(message.Spectrum);
            if (error)
                return "Spectrum." + error;
        }
        return null;
    };

    /**
     * Creates a Transmission message from a plain object. Also converts values to their respective internal types.
     * @param {Object.<string,*>} object Plain object
     * @returns {Transmission} Transmission
     */
    Transmission.fromObject = function fromObject(object) {
        if (object instanceof Transmission)
            return object;
        var message = new Transmission();
        if (object.Timestamp != null)
            if ($util.Long)
                (message.Timestamp = $util.Long.fromValue(object.Timestamp)).unsigned = false;
            else if (typeof object.Timestamp === "string")
                message.Timestamp = parseInt(object.Timestamp, 10);
            else if (typeof object.Timestamp === "number")
                message.Timestamp = object.Timestamp;
            else if (typeof object.Timestamp === "object")
                message.Timestamp = new $util.LongBits(object.Timestamp.low >>> 0, object.Timestamp.high >>> 0).toNumber();
        if (object.Name != null)
            message.Name = String(object.Name);
        if (object.Entropy != null)
            message.Entropy = String(object.Entropy);
        if (object.Spectrum != null) {
            if (typeof object.Spectrum !== "object")
                throw TypeError(".Transmission.Spectrum: object expected");
            message.Spectrum = Spectrum.fromObject(object.Spectrum);
        }
        return message;
    };

    /**
     * Creates a Transmission message from a plain object. Also converts values to their respective internal types.
     * This is an alias of {@link Transmission.fromObject}.
     * @function
     * @param {Object.<string,*>} object Plain object
     * @returns {Transmission} Transmission
     */
    Transmission.from = Transmission.fromObject;

    /**
     * Creates a plain object from a Transmission message. Also converts values to other types if specified.
     * @param {Transmission} message Transmission
     * @param {protobuf.ConversionOptions} [options] Conversion options
     * @returns {Object.<string,*>} Plain object
     */
    Transmission.toObject = function toObject(message, options) {
        if (!options)
            options = {};
        var object = {};
        if (options.defaults) {
            if ($util.Long) {
                var long = new $util.Long(0, 0, false);
                object.Timestamp = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
            } else
                object.Timestamp = options.longs === String ? "0" : 0;
            object.Name = "";
            object.Entropy = "";
            object.Spectrum = null;
        }
        if (message.Timestamp != null && message.hasOwnProperty("Timestamp"))
            if (typeof message.Timestamp === "number")
                object.Timestamp = options.longs === String ? String(message.Timestamp) : message.Timestamp;
            else
                object.Timestamp = options.longs === String ? $util.Long.prototype.toString.call(message.Timestamp) : options.longs === Number ? new $util.LongBits(message.Timestamp.low >>> 0, message.Timestamp.high >>> 0).toNumber() : message.Timestamp;
        if (message.Name != null && message.hasOwnProperty("Name"))
            object.Name = message.Name;
        if (message.Entropy != null && message.hasOwnProperty("Entropy"))
            object.Entropy = message.Entropy;
        if (message.Spectrum != null && message.hasOwnProperty("Spectrum"))
            object.Spectrum = Spectrum.toObject(message.Spectrum, options);
        return object;
    };

    /**
     * Creates a plain object from this Transmission message. Also converts values to other types if specified.
     * @param {protobuf.ConversionOptions} [options] Conversion options
     * @returns {Object.<string,*>} Plain object
     */
    Transmission.prototype.toObject = function toObject(options) {
        return this.constructor.toObject(this, options);
    };

    /**
     * Converts this Transmission to JSON.
     * @returns {Object.<string,*>} JSON object
     */
    Transmission.prototype.toJSON = function toJSON() {
        return this.constructor.toObject(this, protobuf.util.toJSONOptions);
    };

    return Transmission;
})();
