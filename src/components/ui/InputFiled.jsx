export default function InputField({type,placeholder,value,onChange}){

return(

<input
type={type}
placeholder={placeholder}
value={value}
onChange={onChange}
className="border rounded-lg p-3 w-full"
/>

)
}