import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

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
  } = useCurrentButtons();

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
          className="flex items-center justify-center px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-300"
        >
          {button.icon}
          {button.label}
        </button>
      )
    ));
  };

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gray-900">
      <div className="aspect-video max-w-screen-lg w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
          {data?.display_name ?? "Game Title"}
        </h1>
        <div className="flex flex-col space-y-4 mb-16">
          {renderButtons()}
        </div>
      </div>
    </div>
  );
}
