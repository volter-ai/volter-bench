import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as CardBase, 
  CardContent as CardContentBase,
  CardHeader as CardHeaderBase,
  CardTitle as CardTitleBase 
} from "@/components/ui/card"
import { Progress as ProgressBase } from "@/components/ui/progress"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardBase> & BaseProps>(
  ({ uid, ...props }, ref) => <CardBase ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardContentBase> & BaseProps>(
  ({ uid, ...props }, ref) => <CardContentBase ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardHeaderBase> & BaseProps>(
  ({ uid, ...props }, ref) => <CardHeaderBase ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.ComponentProps<typeof CardTitleBase> & BaseProps>(
  ({ uid, ...props }, ref) => <CardTitleBase ref={ref} {...props} />
)

let Progress = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ProgressBase> & BaseProps>(
  ({ uid, ...props }, ref) => <ProgressBase ref={ref} {...props} />
)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={imageUrl}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
Progress.displayName = "Progress"
CreatureCard.displayName = "CreatureCard"

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
Progress = withClickable(Progress)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
