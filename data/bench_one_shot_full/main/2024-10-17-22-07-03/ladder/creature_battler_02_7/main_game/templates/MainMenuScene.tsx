import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const getButtonIcon = (slug: string) => {
    switch (slug) {
      case 'play':
        return <Play className="mr-2 h-4 w-4" />;
      case 'quit':
        return <X className="mr-2 h-4 w-4" />;
      default:
        return null;
    }
  }

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col justify-between items-center p-8">
      <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
        Creature Battle Game
      </h1>
      
      <Card className="p-6 bg-opacity-80 backdrop-blur-sm">
        <div className="flex flex-col space-y-4">
          {availableButtonSlugs.map((slug) => (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="w-full"
            >
              {getButtonIcon(slug)}
              {slug.charAt(0).toUpperCase() + slug.slice(1)}
            </Button>
          ))}
        </div>
      </Card>

      <div className="text-white text-sm mt-4">
        {data.entities.player && (
          <p>Welcome, {data.entities.player.display_name}!</p>
        )}
      </div>
    </div>
  )
}
