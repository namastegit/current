'use client'


import React from 'react'
import ThemeSwitch from './ThemeSwitch'


function Navbar() {
  
  return (
    <header className="relative inset-0 xl:mx-28 ">
         <nav className='antialiased container flex justify-between items-center p-4 mx-auto'>
            <div className="">
                <img src="/forest-11714.svg" alt="comments_svg" className='w-10 hover:scale-125 transition-all duration-500' />
               </div>





<div className=' '>
    <ThemeSwitch></ThemeSwitch>
    


</div>



    </nav>
    </header>
   
  )
}



export default Navbar