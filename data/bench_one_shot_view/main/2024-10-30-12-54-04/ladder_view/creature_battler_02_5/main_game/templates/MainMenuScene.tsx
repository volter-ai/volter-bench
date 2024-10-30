import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface GameUIData {
  entities: {
    player?: {
      uid: string;
      display_name?: string;
    };
  };
  uid: string;
  display_name?: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const renderButtons = () => {
    const buttonConfig = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2" /> },
    ];

    return buttonConfig.map(button => (
      availableButtonSlugs.includes(button.id) && (
        <button
          key={button.id}
          onClick={() => emitButtonClick(button.id)}
          className="flex items-center justify-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          {button.icon}
          {button.label}
        </button>
      )
    ));
  };

  return (
    <div className="w-full h-0 pb-[56.25%] relative" key={data.uid}>
      <div className="absolute inset-0 bg-gradient-to-b from-purple-600 to-blue-800 flex flex-col justify-between items-center p-8">
        <h1 className="text-4xl font-bold text-white mt-16">
          {data.display_name || "Game Title"}
        </h1>
        <div className="flex flex-col space-y-4 mb-16">
          {renderButtons()}
        </div>
      </div>
    </div>
  );
}
