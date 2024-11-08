import {useCurrentButtons} from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Skill {
    uid: string
    stats: {
        base_damage: number
    }
    meta: {
        prototype_id: string
        category: string
        skill_type: string
    }
    display_name: string
    description: string
}

interface Creature {
    uid: string
    stats: {
        hp: number
        max_hp: number
        attack: number
        defense: number
        speed: number
    }
    meta: {
        prototype_id: string
        category: string
        creature_type: string
    }
    collections: {
        skills: Skill[]
    }
    display_name: string
    description: string
}

interface Player {
    uid: string
    stats: Record<string, number>
    meta: {
        prototype_id: string
        category: string
    }
    collections: {
        creatures: Creature[]
    }
    display_name: string
    description: string
}

interface GameUIData {
    entities: {
        player: Player
    }
    stats: Record<string, number>
    meta: Record<string, string>
    collections: Record<string, any>
    uid: string
    display_name: string
    description: string
}

// Note: This component doesn't currently use custom UI components that require UID propagation.
// If adding custom UI components, ensure UIDs are passed through from the data structure.
export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-screen bg-gradient-to-b from-slate-900 to-slate-800 flex items-center justify-center">
            <div className="relative w-full max-w-[177.78vh] h-full max-h-[56.25vw]">
                <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                    {/* Title Section */}
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            {props.data?.display_name || "GAME TITLE"}
                        </h1>
                    </div>

                    {/* Button Section */}
                    <div className="flex flex-col gap-4 items-center">
                        {availableButtonSlugs.includes('play') && (
                            <button
                                onClick={() => emitButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-blue-600 hover:bg-blue-700 
                                         text-white rounded-lg text-xl transition-colors"
                            >
                                <Play size={24} />
                                Play Game
                            </button>
                        )}

                        {availableButtonSlugs.includes('quit') && (
                            <button
                                onClick={() => emitButtonClick('quit')}
                                className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 
                                         text-white rounded-lg text-xl transition-colors"
                            >
                                <X size={24} />
                                Quit
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
