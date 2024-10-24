import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface GameUIData {
    entities: {
        player: {
            uid: string,
            stats: {
                [key: string]: number,
            },
            [key: string]: any,
        }
        [key: string]: any,
    }
    [key: string]: any,
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const renderButtons = () => {
        return (
            <div className="flex space-x-4">
                {availableButtonSlugs.includes('play') && (
                    <button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center justify-center px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                    >
                        <Play className="mr-2" size={24} />
                        Play
                    </button>
                )}
                {availableButtonSlugs.includes('quit') && (
                    <button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center justify-center px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    >
                        <X className="mr-2" size={24} />
                        Quit
                    </button>
                )}
            </div>
        );
    };

    return (
        <div className="w-full h-full bg-gradient-to-b from-blue-900 to-purple-900 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
            <h1 className="text-6xl font-bold text-white mt-16">
                {props.data.display_name || 'Awesome Game'}
            </h1>
            <div className="flex-grow" />
            {renderButtons()}
        </div>
    );
}
