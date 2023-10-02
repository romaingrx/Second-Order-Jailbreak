import AllLinkChips from "@/components/linkChips";

function Layout({ children }) {
  return (
    <>
      <div className="flex flex-col min-h-screen gap-2 py-4">
        <div className="flex flex-col gap-2 justify-center items-center mb-4">
          <h1 className="text-4xl font-bold">Second-order Jailbreaks</h1>
          <p className="text-md text-zinc-700">
            Mikhail Terekhov, Romain Graux, Denis Rosset, Eduardo Neville, Gabin
            Kolly
          </p>
        </div>
        <div className="flex flex-row gap-4 justify-center items-center">
          <AllLinkChips />
        </div>
        <p className="text-md text-zinc-700 w-4/5 sm:w-2/3 md:w-1/2 mx-auto">
          We examine the risk of powerful malignant intelligent actors spreading
          their influence over networks of agents with varying intelligence and
          motivations. We demonstrate this problem through the lens of two
          simplified setups with two or three agents powered by Large Language
          Models (LLMs). Our experiments demonstrate that the smartest available
          models today are already powerful enough to “exploit” other agents and
          extract protected information from them. What is more, they can do so
          even when communicating with the information holder through supposedly
          vigilant observers, who also do not want them to learn the protected
          information and who do not know it themselves. These results provide
          concerning early evidence that an advanced AI can get out of the box
          even in a “distributed privilege” scenario, where the operator that
          this AI talks to cannot release the AI, but the operator has access to
          someone who could release it.
        </p>
        {children}
      </div>
    </>
  );
}
``;
export default Layout;
