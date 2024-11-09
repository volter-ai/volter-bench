import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'

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
    entities: Record<string, unknown>
    collections: Record<string, unknown>
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
    entities: Record<string, unknown>
    collections: {
        skills: Skill[]
    }
    display_name: string
    description: string
}

interface Player {
    uid: string
    stats: Record<string, unknown>
    meta: {
        prototype_id: string
        category: string
    }
    entities: Record<string, unknown>
    collections: {
        creatures: Creature[]
    }
    display_name: string
    description: string
}

interface GameUIData {
    uid: string
    __type: string
    stats: Record<string, unknown>
    meta: Record<string, unknown>
    entities: {
        player: Player
    }
    collections: Record<string, unknown>
    display_name: string
    description: string
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8" key={props.data.uid}>
                {/* Title Section with Image Placeholder */}
                <div className="flex-1 flex items-center justify-center">
                    <div className="w-96 h-32 bg-slate-700 flex items-center justify-center text-slate-500">
                        {/* This div represents where the title image would be placed */}
                        <span className="text-lg">Title Image Placeholder</span>
                    </div>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs?.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-colors"
                        >
                            <Play className="w-6 h-6" />
                            <span className="text-xl font-semibold">Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-colors"
                        >
                            <Power className="w-6 h-6" />
                            <span className="text-xl font-semibold">Quit</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
