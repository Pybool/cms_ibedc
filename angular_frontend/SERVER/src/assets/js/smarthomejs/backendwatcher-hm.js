console.log("In server poller")
self.addEventListener("message", ((e)=>{
    let pollInterval;
    let worker_functions = {} //Functions used by callback
    let args = [] //Arguments of the callback

    for (fn of e.data.functions) {
        worker_functions[fn.name] = new Function(fn.args, fn.body)
        args.push(fn.name)
    }
    
    let callback = new Function( e.data.callback.args, e.data.callback.body) //Callback passed and ready to be executed    
    args = args.map((fn_name) => { return worker_functions[fn_name] }) //FUnctions loaded as arguments
    const fnApply = (async ()=>{
        let result = await callback.apply(null, args) //executing callback with function arguments
        console.log("Backend Web worker poll result ===> ",result)
        if(result==true){
            clearInterval(pollInterval); 
        }
        self.postMessage( result )
        return result
    })
    pollInterval = setInterval(fnApply, 10000);
    
    
}))


