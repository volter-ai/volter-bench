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

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div 
            className="relative w-full h-0 pb-[56.25%] bg-cover bg-center bg-slate-900"
            style={{
                backgroundImage: props.data?.meta?.background_image ? 
                    `url(${props.data.meta.background_image})` : 
                    'linear-gradient(to bottom, rgb(15 23 42), rgb(30 41 59))'
            }}
        >
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider drop-shadow-lg">
                        {props.data?.display_name || "GAME TITLE"}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs?.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-colors shadow-lg"
                        >
                            <Play className="w-6 h-6" />
                            <span className="text-xl font-semibold">Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-colors shadow-lg"
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
