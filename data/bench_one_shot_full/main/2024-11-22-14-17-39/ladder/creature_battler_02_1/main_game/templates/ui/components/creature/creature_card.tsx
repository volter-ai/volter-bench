import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as BaseCard, 
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader, 
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CardProps extends React.ComponentProps<typeof BaseCard> {
  uid: string
}

interface CardContentProps extends React.ComponentProps<typeof BaseCardContent> {
  uid: string
}

interface CardHeaderProps extends React.ComponentProps<typeof BaseCardHeader> {
  uid: string
}

interface CardTitleProps extends React.ComponentProps<typeof BaseCardTitle> {
  uid: string
}

let Card = withClickable(React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
))

let CardContent = withClickable(React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
))

let CardHeader = withClickable(React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
))

let CardTitle = withClickable(React.forwardRef<HTMLParagraphElement, CardTitleProps>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
))

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
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
              className="w-full h-48 object-contain"
            />
            <div className="flex justify-between">
              <span>HP:</span>
              <span>{hp}/{maxHp}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
