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
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  }

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-900 to-purple-900 flex flex-col justify-between items-center p-8">
      <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
        {props.data.display_name || 'Game Title'}
      </h1>

      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig]
          if (!config) return null

          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="flex items-center justify-center space-x-2 bg-white text-blue-900 px-6 py-3 rounded-full font-semibold text-lg hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-200"
            >
              {config.icon && <config.icon className="w-5 h-5" />}
              <span>{config.text}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
