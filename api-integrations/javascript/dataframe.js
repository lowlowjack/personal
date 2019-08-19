
function Dataframe(data){
  // Dataframe object used to manipulate data. Can do some SQL operations on this except for the joins.
  // Note that all data will be parsed in the format of array of array.
  // If number is in string, it will not be parsed as int or float. You have to map it yourself.
  for (i=0;i<data[0].length;i++){
    var g = function(x,z){return x[z]}
    var f = function(z){return g(z,i)}
    this[data[0][i]]={values: data.slice(1).map(f),position:i} 
  }
  this.shape=function(){
   return [this[this.columns[0]].values.length,this.columns.length] 
  }
  
  
  this.print =function(){
    f=this
    var ls = this.columns.reduce(
    function(s,x){
      s.push([x].concat(f[x].values))
      return s
    },[]
  )
  var ls = ls.sort(function(x,y){return f[x[0]].position-f[y[0]].position})
    // Resorts the alignment back to row then column
  return ls.reduce(
    function(s,x){
      var k = x.map(function(y){return [y]})
      return s.map(function(y,i){return y.concat(k[i])})
  }
    ,ls[0].map(function(y){return []}))
  }
  this.rename= function(dict){
    // Renames the columns
    var cpy = Object.create(this)
    const col = Object.create(this.columns)
    do{ var key=col.shift(1)
    if (dict[key]){
      this[dict[key]]=cpy[key] 
      delete this[key]
    }
      } while (col.length>0)
    this.columns=this.getcolumns()
    return this

  }
  this.reposition= function(newposition){
    const col = Object.create(this.columns)
    do { var key=col.shift(1)
      this[key].position = (newposition[key]+1 || this[key].position+1)-1
    } while (col.length>0)
    return this
  }
  this.union= function(df2){
    // Unions two Dataframes
    var f = this
    
    // Memory storage to figure out how many missing values to put in. 
    const m1 = this[this.columns[0]].values.length
    const m2 = df2[df2.columns[0]].values.length
    // Join all the keys
    var h = this.columns.concat(df2.columns)
    do{
      var key = h.shift(1)
      if (this.columns.indexOf(key)>=0){
        if (df2.columns.indexOf(key)>=0){
          // If both are met, concatentate and remove the additional key
          this[key]={values:f[key].values.concat(df2[key].values),position:f[key].position}
          var h = h.filter(function(y){return y!=key})
        }
        else {
          // Otherwise, reshape the array to have the correct shape
          this[key]={values:f[key].values.concat(Array(m2)),position:f[key].position}
        }
      }
      else {
        this[key]={values:Array(m1).concat(df2[key].values),position:this.columns.length}
      }
    } while (h.length>0)
      this.columns=this.getcolumns()
    return this 
  }
  this.assign=function(functiondict){
    const cpy = Object.create(this)
    for (name in functiondict){
      var fn = functiondict[name]
      if ((fn instanceof Array) && (fn.length=this.shape()[0])){
        var f = function(x,i){return fn[i]}
        } 
      else if (!(fn instanceof Function)){
        var f = function(x){return fn}
        } 
        
        else{
          var f = fn 
          }
      try {
        this[name]={values:cpy[name].values.map(f),position:this.shape()[1]} 
      } catch(e){
        this[name]={values:cpy[cpy.columns[0]].values.map(f),position:this.shape()[1]}
      }
    }
    this.columns=this.getcolumns()
    return this
  }
  this.getcolumns=function(){
    var f=this
    return Object.keys(f).filter(function(x){return !(f[x] instanceof Function) && x!='columns'})
    
  }
  this.columns=this.getcolumns()
  this.leftjoin=function(y){
  }
  this.slice= function(){
    // Slices the Dataframe. Works same as Array slice
    var k =arguments
   if (!k[1]){
     k[1]=this[this.columns[0]].values.length 
     }
    // Converting to array first to break all the object references.
    var cpy = this.print()
    var cpy = [cpy[0]].concat(cpy.slice(1).slice(k[0],k[1]))
    
    var cpy = new Dataframe(cpy)
    return cpy
  }
  this.query=function(filter,key){
    // Filter is a function that returns a boolean value. Boolean is evaluated element wise on key to query.
    var cpy = Object.create(this)
    var condition = cpy[key].values.map(filter)
     const col = Object.create(this.columns)
     col.reduce(function(s,x){s[x].values=s[x].values.filter(function(x,i){return condition[i]}); return s},cpy)
    return cpy
    
  }
  this.colslice=function(keyarray){
    // Returns a modified Dataframe with the assoicated object properties in key removed. Includes functions and columns.
    // Does not modify existing Dataframe
    var cpy ={}
    for (k in this){
      if (keyarray.indexOf(k)<0){
        cpy= Object.defineProperty(cpy, k, Object.getOwnPropertyDescriptor(this,k))
      }
    }
    cpy.columns=cpy.getcolumns()
    return cpy
  }
  this.groupmap=function(iter,fmap){
   // This groups the Dataframe by the iter and then reduces the remaining columns using fmap
    // Order everything first.
    var df = this.order(iter)
    var k = df.colslice(this.columns.filter(function(x){return iter.indexOf(x)<0})).print()
    k.shift()
    var k = k.map(function(x){return x.join()})
    var r=[0]
    do {
      var l = k.lastIndexOf(k[0])
      k.splice(0,l+1)
      r.push(r[r.length - 1]+l+1)
    } while (k.length>0)
      do{   
        k.push(df.slice(r[0],r[1]))
        r.shift()
      } while(r.length>1)
        var ffmap = Object.create(fmap)
        var f = function(s,x){
         return s||x 
        }
        for (i in iter){
         ffmap[iter[i]]=f 
        }
        return k.reduce(function(s,x){
          return s.union(x.reduce(ffmap))},
        new Dataframe([[df.columns[0]]])
        )

  }
  this.order=function(iter){
    var cpy = this.print()
    var index= iter.map(function(x){return cpy[0].indexOf(x)})
    
    callback = function(x,y){
      return index.reduce(function(s,i){
        if (s !=0){
          return s
        }
        if (x[i]<y[i]){
          return -1 
        }
        else if (x[i]>y[i]) { 
          return 1}
        else if (x[i]==null){
          return -1
        }
        else if (y[i]==null){
          return -1
        }
        else { return s} 
      },0)
    }
    return new Dataframe([cpy[0]].concat(cpy.slice(1).sort(callback)))
  }
  this.reduce=function(fmap){
     var cpy = new Dataframe(this.print())
     for (i in fmap){
      cpy[i].values=[cpy[i].values.reduce(fmap[i])]
     }
     return cpy
  }
  this.ljoin=function(df,joinkeys){
    if (joinkeys instanceof Array){
      var jk = {}
      for (i in joinkeys){
       jk[joinkeys[i]]= jk[joinkeys[i]]
      }
    }
    else{ var jk = Object.create(joinkeys)}
    var cpyl = this.order(Object.keys(jk))
    var cpyr = df.order(Object.keys(jk).map(function(x){return jk[x]}))
    var lkeys= cpyl.colslice(cpyl.columns.filter(function(x){return Object.keys(jk).indexOf(x)<0})).print()
    var rkeys= cpyr.colslice(cpyl.columns.filter(function(x){return Object.keys(jk).map(function(x){return jk[x]}).indexOf(x)<0})).print()
    lkeys.shift()
    rkeys.shift()
    do{
      
    } while (lkeys.length>0)

  }
}
