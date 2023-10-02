function Layout({ children }) {
  return (
    <>
      <div className="flex flex-col min-h-screen gap-4 py-4">
        <div className="flex flex-col gap-2 justify-center items-center mb-4">
          <h1 className="text-4xl font-bold">Second-order Jailbreaks</h1>
          <p className="text-md text-zinc-700">
            Mikhail Terekhov, Romain Graux, Denis Rosset, Eduardo Neville, Gabin
            Kolly
          </p>
        </div>
        {children}
      </div>
    </>
  );
}

export default Layout;
