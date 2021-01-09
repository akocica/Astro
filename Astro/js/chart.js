
var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S.%L");
bd.forEach(function(d) {
	d.dt = new Date(parseTime(d.t).getTime() - 1000*60*60*4);
	d.y = +d.v;
});

var margin = { top:16, right:32, bottom:32, left:64 },
	width = 800 - margin.left - margin.right,
	height = 400 - margin.top - margin.bottom;

function xGrid() { return d3.axisBottom(x).ticks(10) }
function yGrid() { return d3.axisLeft(y).ticks(10) }

var [sd, ed] = d3.extent(bd, function(d) {return d.dt;});
var x = d3.scaleTime().domain([sd, ed]).range([0, width]).nice();
var y = d3.scaleLinear().range([height, 0]);

x.domain(d3.extent(bd, function(d) { return d.dt; } ));
y.domain(d3.extent(bd, function(d) { return d.v   } ));

var valueline = d3.line()
	.x(function(d) { return x(d.dt); })
	.y(function(d) { return y(d.v);  });


var svg = d3.select("#chart").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("path").data([bd]).attr("class", "line").attr("d", valueline);


svg.append("g").attr("class", "xax")
	.attr("transform", "translate(0," + height + ")")
	.call(d3.axisBottom(x).tickFormat(d3.timeFormat("%m-%d %H")));

svg.append("g").attr("class", "yax")
	.call(d3.axisLeft(y));

svg.append("g").attr("class", "grid")
	.attr("transform", "translate(0," + height + ")")
	.call(xGrid().tickSize(-height).tickFormat(""))

svg.append("g").attr("class", "grid")
	.call(yGrid().tickSize(-width).tickFormat(""))

//d3.select(".yax").style("font-size","16px");


function update(data) {

	x.domain(d3.extent(bd, function(d) { return d.dt; } ));
	y.domain(d3.extent(bd, function(d) { return d.v   } ));

	d3.axisBottom().scale(x);
	d3.axisLeft().scale(y);

	var q = d3.select("#chart").transition();

	q.select(".line")
		.duration(750)
		.attr("d", valueline(bd));
	q.select(".xax")
		.duration(750)
		.call(d3.axisBottom(x));
	q.select(".yax")
		.duration(750)
		.call(d3.axisLeft(y));
			
}


///////////////////////////////////////////////////

var mqtt;
var reconnectTimeout = 2000;
var host = "54.165.14.106"
var port = 9001;

function onFailure(message) {
	report("MQTT Failed ["+host+":"+port+"]");
	setTimeout(MQTTconnect, reconnectTimeout);
}

function onMessageArrived(msg){
	document.getElementById("message").innerHTML = "["+msg.destinationName+"]:"+msg.payloadString;
	if(msg.payloadString.trim().substring(0,1) === "{"){
		try {
			var obj = JSON.parse(msg.payloadString);
			console.log(obj);
			bd.push({"dt":new Date(),"v":obj.p, "y":+obj.p})
			update(bd);
		}
		catch(err) {
			console.log(err.message);
		}
	}
}

function onConnect() {
	report("MQTT Connected ["+host+":"+port+"]");
	mqtt.subscribe("owntracks/#");
	message = new Paho.MQTT.Message("Connected");
	message.destinationName = "owntracks/user/Browser";
	mqtt.send(message);
}

function MQTTconnect() {
	report("MQTT Connecting ["+host+":"+port+"]");
	mqtt = new Paho.MQTT.Client(host, port, "Browser");
	var options = { timeout: 3, onSuccess: onConnect, onFailure: onFailure };
	mqtt.onMessageArrived = onMessageArrived
	mqtt.connect(options);
}


function report(cl) {
	console.log(cl);
	document.getElementById("status").innerHTML = cl;
}

MQTTconnect();
