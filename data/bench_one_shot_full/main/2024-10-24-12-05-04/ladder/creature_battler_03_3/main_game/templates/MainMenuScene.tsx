import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
// import {Card} from "@/components/ui/card";

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
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  }

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between p-8">
      <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
        {data.display_name || 'Awesome Game'}
      </h1>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig]
          if (!config) return null
          
          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white text-purple-600 font-semibold py-2 px-6 rounded-full shadow-lg hover:bg-purple-100 transition duration-300 flex items-center space-x-2"
            >
              <config.icon className="w-5 h-5" />
              <span>{config.text}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
