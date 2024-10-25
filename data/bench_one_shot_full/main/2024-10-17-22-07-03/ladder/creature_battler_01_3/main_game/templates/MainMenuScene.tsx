import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, number>;
  meta: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const renderButtons = () => {
    const buttons = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2" /> },
    ];

    return buttons.map(button => (
      availableButtonSlugs.includes(button.id) && (
        <button
          key={button.id}
          onClick={() => emitButtonClick(button.id)}
          className="flex items-center justify-center px-6 py-3 mb-4 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-200"
        >
          {button.icon}
          {button.label}
        </button>
      )
    ));
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-purple-900 to-blue-900 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-5xl font-bold text-white mb-8 mt-16">Game Title</h1>
      <div className="flex flex-col items-center mb-16">
        {renderButtons()}
      </div>
    </div>
  );
}
