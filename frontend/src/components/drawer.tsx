type IDrawer = {
  isOpen: boolean
  setIsOpen: (isOpen: boolean) => void
}

export function Drawer({ isOpen, setIsOpen }: IDrawer) {
  console.log("Drawer")
  return (
    <main
      className={
        " fixed overflow-hidden z-50 bg-gray-900 bg-opacity-25 inset-0 transform ease-in-out " +
        (isOpen
          ? " transition-opacity opacity-100 duration-500 translate-y-0  "
          : " transition-all delay-500 opacity-0 translate-y-full  ")
      }>
      <section
        className={
          " h-screen max-h-36 bottom-0 absolute bg-white w-full shadow-xl delay-400 duration-500 ease-in-out transition-all transform text-xs " +
          (isOpen ? " translate-y-0 " : " translate-y-full ")
        }>
        <div className='p-4 text-gray-700'>
          <p>
            This project is made for fun. promptAnnARTS is about arts and
            nothing about nvidia's RTS. Of course you should have a RTS to run
            stable diffusion, but that's not the point, the point is I'm
            learning react and typescript.
          </p>
          <p>
            When I swim in the sea of Stable Diffusion, I got good pictures
            accidentally, I want to remember the good things and forget the bad,
            so I made this little app for help.
          </p>
          <p className='text-gray-400'>It could help you either, I hope.</p>
          <p className='float-right text-gray-300'>
            {" "}
            - xdream oldlu: an old student
          </p>
          <p>
            <br />
            <a
              className='bg-gray-200 rounded-full px-2'
              href='https://github.com/deadlyedge/promptAnnARTS/'>
              Page on GITHUB
            </a>
          </p>
        </div>
      </section>
      <section
        className=' h-screen w-full cursor-pointer '
        onClick={() => setIsOpen(false)}></section>
    </main>
  )
}
