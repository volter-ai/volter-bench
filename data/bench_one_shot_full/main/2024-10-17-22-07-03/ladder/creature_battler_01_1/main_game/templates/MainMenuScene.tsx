import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";

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
  uid: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const renderButtons = () => {
    const buttons = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2" size={20} /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2" size={20} /> },
    ];

    return buttons.map(button => (
      availableButtonSlugs.includes(button.id) && (
        <Button
          key={button.id}
          onClick={() => emitButtonClick(button.id)}
          className="flex items-center justify-center px-6 py-3 mb-4 text-lg font-semibold"
        >
          {button.icon}
          {button.label}
        </Button>
      )
    ));
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-900 to-purple-900 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-5xl font-bold text-white mb-8 mt-16">Game Title</h1>
      <div className="flex flex-col items-center mb-16">
        {renderButtons()}
      </div>
    </div>
  );
}
