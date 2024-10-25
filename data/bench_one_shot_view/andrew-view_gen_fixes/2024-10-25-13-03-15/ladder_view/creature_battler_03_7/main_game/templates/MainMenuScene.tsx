// Do not change these imports:
import {useCurrentButtons} from "@/lib/useChoices.ts";

// Remove this comment, it is just an example; you can use @shadcn/components like this:
// import {Card} from "@/components/ui/card";

// You can change this import:
import { Play, X } from 'lucide-react'

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
        // numerical properties go in here
    },
    // other properties like collections, metas, and entities go here
}

interface GameUIData {
    entities: {  // dictionary of Things such as player
        player: ExamplePlayer
        // other entities go here. Such as opponent, etc.
    }
    // other fields e.g. stats, meta goes here
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        play: { text: 'Play', icon: Play },
        quit: { text: 'Quit', icon: X },
    }

    return (
        <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white text-center">
                    {props.data?.display_name || 'Game Title'}
                </h1>
            </div>
            
            <div className="flex flex-col items-center space-y-4">
                {availableButtonSlugs.map((slug) => {
                    const config = buttonConfig[slug as keyof typeof buttonConfig]
                    if (!config) return null
                    
                    return (
                        <button
                            key={slug}
                            onClick={() => emitButtonClick(slug)}
                            className="flex items-center justify-center space-x-2 bg-white text-purple-600 px-8 py-3 rounded-full text-xl font-semibold hover:bg-opacity-90 transition-colors"
                        >
                            <config.icon className="w-6 h-6" />
                            <span>{config.text}</span>
                        </button>
                    )
                })}
            </div>
        </div>
    )
}
