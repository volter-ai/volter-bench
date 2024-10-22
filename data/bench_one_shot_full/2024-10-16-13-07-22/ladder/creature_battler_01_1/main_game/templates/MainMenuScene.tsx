import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: {
    creatures: Array<{
      uid: string;
      display_name: string;
      description: string;
      stats: {
        hp: number;
        max_hp: number;
      };
      collections: {
        skills: Array<{
          uid: string;
          display_name: string;
          description: string;
          stats: {
            damage: number;
          };
        }>;
      };
    }>;
  };
  display_name: string;
  description: string;
}

interface GameUIData {
  __type: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: {
    player: Player;
  };
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
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
      { id: 'play', label: 'Play', icon: <Play className="mr-2 h-4 w-4" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2 h-4 w-4" /> },
    ];

    return buttons.map(button => (
      availableButtonSlugs.includes(button.id) && (
        <Button
          key={button.id}
          onClick={() => emitButtonClick(button.id)}
          className="w-48 flex items-center justify-center"
        >
          {button.icon}
          {button.label}
        </Button>
      )
    ));
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8">
      <h1 className="text-4xl font-bold mt-16">
        {data.display_name || "Game Title"}
      </h1>
      <div className="mt-auto mb-16 space-y-4">
        {renderButtons()}
      </div>
    </div>
  );
}
