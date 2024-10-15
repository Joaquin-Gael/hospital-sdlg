import {MercadoPagoConfig,Preference} from 'mercadopago';

const API_URL = 'http://127.0.0.1:8000/'; 
const client = new MercadoPagoConfig({ accessToken: "YOUR_ACCESS_TOKEN"});

const post = async(req,res)=>{
    try{
        const body = {
            items: [
               {
                title: req.body.title,
                unit_price: Number(req.body.unit_price),        
                currency_id: "ARS",
               },
            ],
            back_urls: {
                success: "https://54bb-181-228-78-24.ngrok-free.app/user/panel",
                failure: " https://54bb-181-228-78-24.ngrok-free.app",
                pending: " https://54bb-181-228-78-24.ngrok-free.app",
            },
            auto_return: "approved",
       };

       const preference = new Preference(client);
       const result = await preference.create({body})
       res.json({
        id: result.id,
       })
       const resp = await fetch(`${API_URL}/create_preference/`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    })
    }catch(error){
        console.log("Error: ", error.message)
    } 
}
