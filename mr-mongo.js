DBQuery.shellBatchSize = 200;
m = function() { 
	emit(this.category,1) 
};

r = function(k,vals) { 
	var sum = 0;  
	for(var i=0; i < vals.length; i++) { 
		sum += vals[i];
	} 
	return sum;     
};

res = db.people.mapReduce(m, r, "Category:" );
db[res.result].find()