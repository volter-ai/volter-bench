import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'

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
    stats: Record<string, number>
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

    const buttonConfig = {
        play: { icon: Play, label: 'Play Game' },
        quit: { icon: XCircle, label: 'Quit Game' }
    }

    return (
        <div className="w-full h-full flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data?.display_name || 'Game Title'}
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs?.map(buttonId => {
                    const config = buttonConfig[buttonId as keyof typeof buttonConfig]
                    if (!config) return null

                    const Icon = config.icon

                    return (
                        <button
                            key={buttonId}
                            onClick={() => emitButtonClick(buttonId)}
                            className="flex items-center gap-3 px-8 py-4 bg-slate-700 hover:bg-slate-600 
                                     text-white rounded-lg transition-colors duration-200 min-w-[200px]
                                     justify-center"
                        >
                            <Icon size={24} />
                            <span className="text-xl">{config.label}</span>
                        </button>
                    )
                })}
            </div>
        </div>
    )
}
