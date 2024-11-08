import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'

interface ExamplePlayer {
    uid: string,
    stats: Record<string, number>,
    meta: {
        prototype_id: string,
        category: string
    },
    collections: {
        creatures?: Array<{
            uid: string,
            stats: Record<string, number>,
            meta: {
                prototype_id: string,
                category: string,
                creature_type: string
            }
        }>
    },
    display_name: string,
    description: string
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

type ButtonSlug = 'play' | 'quit';

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const handleButtonClick = (slug: ButtonSlug) => {
        emitButtonClick(slug)
    }

    return (
        <div className="w-full h-full relative">
            {/* 16:9 container with aspect ratio lock */}
            <div className="absolute inset-0 w-full h-full" style={{aspectRatio: '16/9'}}>
                <div className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-950 flex flex-col justify-between items-center p-8">
                    {/* Title Section */}
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider text-center">
                            {props.data?.entities?.player?.display_name || "Game Title"}
                        </h1>
                    </div>

                    {/* Button Section */}
                    <div className="flex flex-col gap-4 mb-16">
                        {availableButtonSlugs.includes('play') && (
                            <button
                                onClick={() => handleButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <Play size={24} />
                                Play Game
                            </button>
                        )}

                        {availableButtonSlugs.includes('quit') && (
                            <button
                                onClick={() => handleButtonClick('quit')}
                                className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <Power size={24} />
                                Quit
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
