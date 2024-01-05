import { cn } from "@/lib/utils"

type DrawerProps = {
  isOpen: boolean
  setIsOpen: (isOpen: boolean) => void
}

export function Drawer({ isOpen, setIsOpen }: DrawerProps) {
  console.log("Drawer")
  return (
    <main
      className={cn(
        "fixed overflow-hidden z-50 bg-gray-900 bg-opacity-25 inset-0 transform ease-in-out",
        isOpen
          ? "transition-opacity opacity-100 duration-500 translate-y-0"
          : "transition-all delay-500 opacity-0 translate-y-full "
      )}>
      <section
        className={cn(
          "h-screen max-h-36 bottom-0 absolute bg-white w-full shadow-xl delay-400 duration-500 ease-in-out transition-all transform text-xs",
          isOpen ? "translate-y-0" : "translate-y-full"
        )}>
        <div className='p-4 text-gray-700'>
          <p>This project is made for fun.</p>
          <p>
            I throught it may useful when someone have a vps and want to add a
            bit more workload to it, and may make some test work easier.
          </p>
          <p>
            I choose mongodb with gridFS support, because I love mongo, and I
            have had a mongodb running, and it looks less code to write.
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
              href='https://github.com/deadlyedge/pyMongoFileServer'>
              Page on GITHUB
            </a>
          </p>
        </div>
      </section>
      <section
        className='h-screen w-full cursor-pointer'
        onClick={() => setIsOpen(false)}></section>
    </main>
  )
}
