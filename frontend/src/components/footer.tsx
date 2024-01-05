import { useState } from "react"
import { Drawer } from "./drawer"

export function Footer() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div className='fixed w-20 bottom-5 right-5 block z-40'>
        <button
          className='bg-amber-400 p-3 shadow-md transition duration-500 hover:scale-125 hover:bg-amber-100 focus:ring-4 focus:ring-blue-300 font-bold rounded-lg text-sm px-5 py-2.5'
          type='button'
          onClick={() => setIsOpen(true)}>
          About
        </button>
      </div>
      <Drawer isOpen={isOpen} setIsOpen={setIsOpen} />
    </>
  )
}
